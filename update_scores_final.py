import requests
import json

print("=" * 70)
print("🏈 SUPER BOWL LX - AUTOMATIC FIREBASE UPDATE")
print("=" * 70)
print("Final Score: Seattle Seahawks 29 - New England Patriots 13\n")

# Firebase configuration
DB_URL = "https://super-bowl-squares-fam-2026-default-rtdb.firebaseio.com"

# Official quarter scores
scores = {
    "SEA": [3, 9, 7, 10],  # Totals: 3, 12, 19, 29
    "NE": [0, 0, 0, 13]     # Totals: 0, 0, 0, 13
}

meta = {
    "status": "STATUS_FINAL",
    "period": 4,
    "clock": "0:00",
    "detail": "Final",
    "seaTotal": 29,
    "neTotal": 13
}

try:
    # Update directly at root (most Firebase setups store data at root)
    print("📡 Connecting to Firebase...")
    
    # Update scores
    print("\n📊 Updating scores...")
    r1 = requests.patch(f"{DB_URL}/scores.json", json=scores)
    if r1.status_code == 200:
        print("✅ Scores updated successfully!")
    else:
        print(f"⚠️  Scores response: {r1.status_code}")
    
    # Update game metadata
    print("\n⚙️  Updating game metadata...")
    r2 = requests.patch(f"{DB_URL}/gameMeta.json", json=meta)
    if r2.status_code == 200:
        print("✅ Game metadata updated successfully!")
    else:
        print(f"⚠️  Metadata response: {r2.status_code}")
    
    print("\n" + "=" * 70)
    print("✅ FIREBASE UPDATE COMPLETE!")
    print("=" * 70)
    print("\nQuarter Breakdown:")
    print("  Q1: SEA  3 - NE  0  (Winner: Column 3, Row 0)")
    print("  Q2: SEA 12 - NE  0  (Winner: Column 2, Row 0)")
    print("  Q3: SEA 19 - NE  0  (Winner: Column 9, Row 0)")  
    print("  Q4: SEA 29 - NE 13  (Winner: Column 9, Row 3)")
    print("\n🎉 Refresh your app (Ctrl+F5) to see the final results!")
    print("=" * 70)

except requests.exceptions.RequestException as e:
    print(f"\n❌ Connection error: {e}")
    print("\n📝 MANUAL UPDATE REQUIRED")
    print("-" * 70)
    print("Go to: https://console.firebase.google.com/")
    print("Project: super-bowl-squares-fam-2026")
    print("\nUpdate these values:")
    print(f"  scores/SEA: {scores['SEA']}")
    print(f"  scores/NE:  {scores['NE']}")
    print(f"  gameMeta/status: \"{meta['status']}\"")
    print(f"  gameMeta/seaTotal: {meta['seaTotal']}")
    print(f"  gameMeta/neTotal: {meta['neTotal']}")
    print("=" * 70)
except Exception as e:
    print(f"\n❌ Error: {e}")
