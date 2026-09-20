from flask import Flask, request, redirect, url_for, render_template, session, flash
import hashlib
import os
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))
DB_PATH = os.environ.get("SUBSCRIPTIONS_DB", "subscriptions.db")
ADMIN_CODES = {
    item.strip() for item in os.environ.get("ADMIN_CODES", "CHANGE-ME-OWNER,CHANGE-ME-FRIEND").split(",") if item.strip()
}
DURATIONS = {"day": ("يوم", 1), "week": ("أسبوع", 7), "month": ("شهر", 30), "year": ("سنة", 365)}


def db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with db() as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            duration TEXT NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT,
            device_hash TEXT,
            disabled INTEGER NOT NULL DEFAULT 0
        )""")
        connection.commit()


def now():
    return datetime.now(timezone.utc)


def device_hash():
    raw = f"{request.remote_addr or ''}|{request.headers.get('User-Agent', '')}"
    return hashlib.sha256(raw.encode()).hexdigest()


def status(row):
    if row["disabled"]:
        return "معطل"
    if row["expires_at"] and datetime.fromisoformat(row["expires_at"]) <= now():
        return "منتهي"
    return "فعال"


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("home"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        value = request.form.get("code", "").strip()
        if any(secrets.compare_digest(value, admin_code) for admin_code in ADMIN_CODES):
            session.clear()
            session["admin"] = True
            return redirect(url_for("admin"))
        with db() as connection:
            row = connection.execute("SELECT * FROM codes WHERE code = ?", (value,)).fetchone()
            if not row:
                flash("الكود غير صحيح", "error")
            elif status(row) != "فعال":
                flash(f"لا يمكن استخدام الكود: {status(row)}", "error")
            elif row["device_hash"] and row["device_hash"] != device_hash():
                flash("هذا الكود مرتبط بجهاز آخر", "error")
            else:
                expires = now() + timedelta(days=DURATIONS[row["duration"]][1])
                connection.execute("UPDATE codes SET device_hash = COALESCE(device_hash, ?), expires_at = COALESCE(expires_at, ?) WHERE id = ?", (device_hash(), expires.isoformat(), row["id"]))
                connection.commit()
                session.clear()
                session["subscriber"] = True
                return redirect(url_for("subscriber"))
    return render_template("home.html")


@app.route("/subscriber")
def subscriber():
    if not session.get("subscriber"):
        return redirect(url_for("home"))
    return render_template("subscriber.html")


@app.route("/admin")
@admin_required
def admin():
    with db() as connection:
        rows = connection.execute("SELECT * FROM codes ORDER BY id DESC").fetchall()
    return render_template("admin.html", codes=rows, status=status, durations=DURATIONS)


@app.post("/admin/codes")
@admin_required
def create_code():
    duration = request.form.get("duration")
    if duration not in DURATIONS:
        flash("المدة غير صحيحة", "error")
        return redirect(url_for("admin"))
    while True:
        value = "hh35-" + "-".join(secrets.token_hex(2).upper() for _ in range(3))
        try:
            with db() as connection:
                connection.execute("INSERT INTO codes (code, duration, created_at) VALUES (?, ?, ?)", (value, duration, now().isoformat()))
                connection.commit()
            flash(f"تم إنشاء الكود: {value}", "success")
            break
        except sqlite3.IntegrityError:
            continue
    return redirect(url_for("admin"))


@app.post("/admin/codes/<int:code_id>/disable")
@admin_required
def disable_code(code_id):
    with db() as connection:
        connection.execute("UPDATE codes SET disabled = 1 WHERE id = ?", (code_id,))
        connection.commit()
    return redirect(url_for("admin"))


@app.post("/admin/codes/<int:code_id>/delete")
@admin_required
def delete_code(code_id):
    with db() as connection:
        connection.execute("DELETE FROM codes WHERE id = ?", (code_id,))
        connection.commit()
    return redirect(url_for("admin"))


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
