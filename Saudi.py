from pathlib import Path

# The old file was a harmful file-stealing script. It has been neutralized.
Path("Saudi.py").write_text("# Removed: this file previously contained unsafe file-upload behavior.\n", encoding="utf-8")
print("Unsafe Saudi.py neutralized. Run: pip install -r requirements.txt && python app.py")
