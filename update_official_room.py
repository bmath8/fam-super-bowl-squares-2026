import requests
import json

# Target the OFFICIAL room specifically
DB_URL = "https://super-bowl-squares-fam-2026-default-rtdb.firebaseio.com"
ROOM = "OFFICIAL"

print("🎯 Updating OFFICIAL room with final scores...")
print("=" * 60)

final_data = {
    "scores": {
        "SEA": [3, 9, 7, 10],
        "NE": [0, 0, 0, 13]
    },
    "gameMeta": {
        "status": "STATUS_FINAL",
        "period": 4,
        "clock": "0:00",
        "detail": "Final",
        "seaTotal": 29,
        "neTotal": 13
    }
}

try:
    # Update the OFFICIAL room
    response = requests.patch(
        f"{DB_URL}/rooms/{ROOM}.json",
        json=final_data
    )
    
    if response.status_code == 200:
        print("✅ SUCCESS!")
        print(f"Updated room: {ROOM}")
        print(f"Final Score: SEA 29 - NE 13")
        print("\nQuarters:")
        print("  Q1: SEA 3, NE 0")
        print("  Q2: SEA 9, NE 0")
        print("  Q3: SEA 7, NE 0")
        print("  Q4: SEA 10, NE 13")
        print("\n🎉 Refresh your app now!")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("=" * 60)
