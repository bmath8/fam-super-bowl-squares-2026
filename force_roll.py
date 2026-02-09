import requests
import random
import time

url = "https://super-bowl-squares-fam-2026-default-rtdb.firebaseio.com/rooms/OFFICIAL.json"

# 1. Fetch current data to preserve feed
try:
    resp = requests.get(url)
    current_data = resp.json() if resp.status_code == 200 else {}
    feed = current_data.get("feed", [])
except:
    feed = []

# 2. Randomize 0-9
cols = list(range(10))
random.shuffle(cols)
rows = list(range(10))
random.shuffle(rows)

# 3. Add to feed
new_event = {
    "who": "SYSTEM",
    "msg": "Forced board lock and random assign.",
    "ts": int(time.time() * 1000),
    "cat": "Admin"
}
feed.append(new_event)

# 4. Patch data
payload = {
    "isLocked": True,
    "colNums": cols,
    "rowNums": rows,
    "feed": feed
}

print(f"Randomizing numbers for OFFICIAL room...")
r = requests.patch(url, json=payload)

if r.status_code == 200:
    print("✅ SUCCESS: Board locked and numbers assigned!")
    print(f"SEA Numbers: {cols}")
    print(f"NE Numbers: {rows}")
else:
    print(f"❌ FAILED: {r.status_code}")
    print(r.text)
