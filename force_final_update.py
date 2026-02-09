import requests
import json

DB_URL = "https://super-bowl-squares-fam-2026-default-rtdb.firebaseio.com"

print("🔍 Diagnosing Firebase database structure...\n")

# Check what's actually in the database
response = requests.get(f"{DB_URL}.json")
data = response.json()

if data:
    print("✓ Database contains data")
    print(f"Root keys: {list(data.keys())}\n")
    
    # Check current scores
    if 'scores' in data:
        print(f"Current scores at root: {data['scores']}")
    
    if 'gameMeta' in data:
        print(f"Current gameMeta at root: {data['gameMeta']}")
    
    # Now let's force update with the correct final scores
    print("\n" + "=" * 70)
    print("🔧 FORCING FINAL SCORE UPDATE...")
    print("=" * 70)
    
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
    
    # Force overwrite
    update_response = requests.patch(f"{DB_URL}.json", json=final_data)
    
    if update_response.status_code == 200:
        print("✅ FORCED UPDATE SUCCESSFUL!")
        print("\nFinal Scores Set:")
        print("  Q1: SEA 3 - NE 0")
        print("  Q2: SEA 9 - NE 0")  
        print("  Q3: SEA 7 - NE 0")
        print("  Q4: SEA 10 - NE 13")
        print("\n  FINAL: SEA 29 - NE 13")
        print("\n🎉 Hard refresh (Ctrl+F5) NOW to see updated scores!")
    else:
        print(f"❌ Update failed: {update_response.status_code}")
        print(f"Response: {update_response.text}")
else:
    print("❌ Database appears empty")

print("=" * 70)
