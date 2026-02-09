import requests
import json

# Firebase REST API endpoint
DATABASE_URL = "https://super-bowl-squares-fam-2026-default-rtdb.firebaseio.com"

# Final scores from Super Bowl LX
final_scores = {
    "SEA": [3, 9, 7, 10],  # Q1: 3, Q2: 9, Q3: 7, Q4: 10 = 29 total
    "NE": [0, 0, 0, 13]     # Q1: 0, Q2: 0, Q3: 0, Q4: 13 = 13 total
}

game_meta = {
    "status": "STATUS_FINAL",
    "period": 4,
    "clock": "0:00",
    "detail": "Final",
    "seaTotal": 29,
    "neTotal": 13
}

print("🏈 Updating Firebase with Super Bowl LX Final Scores...")
print("=" * 60)
print("SEA 29 - NE 13")
print("=" * 60)

# First, let's find the pool ID by getting the database structure
try:
    response = requests.get(f"{DATABASE_URL}/pools.json")
    pools = response.json()
    
    if pools:
        # Get the first (and likely only) pool
        pool_id = list(pools.keys())[0]
        print(f"✓ Found pool: {pool_id}")
        
        # Update scores
        print("\n📊 Updating scores...")
        scores_response = requests.patch(
            f"{DATABASE_URL}/pools/{pool_id}/scores.json",
            data=json.dumps(final_scores)
        )
        
        if scores_response.status_code == 200:
            print("✓ Scores updated successfully!")
            print(f"  SEA: {final_scores['SEA']}")
            print(f"  NE:  {final_scores['NE']}")
        else:
            print(f"✗ Failed to update scores: {scores_response.status_code}")
            print(f"  Response: {scores_response.text}")
        
        # Update game metadata
        print("\n⚙️  Updating game metadata...")
        meta_response = requests.patch(
            f"{DATABASE_URL}/pools/{pool_id}/gameMeta.json",
            data=json.dumps(game_meta)
        )
        
        if meta_response.status_code == 200:
            print("✓ Game metadata updated successfully!")
            print(f"  Status: {game_meta['status']}")
            print(f"  Final Score: SEA {game_meta['seaTotal']} - NE {game_meta['neTotal']}")
        else:
            print(f"✗ Failed to update metadata: {meta_response.status_code}")
            print(f"  Response: {meta_response.text}")
        
        print("\n" + "=" * 60)
        print("✅ DATABASE UPDATE COMPLETE!")
        print("=" * 60)
        print("\nWinners by quarter (last digit):")
        print("  Q1: Column 3, Row 0 (SEA 3, NE 0)")
        print("  Q2: Column 2, Row 0 (SEA 12, NE 0)")
        print("  Q3: Column 9, Row 0 (SEA 19, NE 0)")
        print("  Q4: Column 9, Row 3 (SEA 29, NE 13)")
        print("\n🎉 Refresh your app to see the final results!")
        
    else:
        print("✗ No pools found in database")
        print("  You may need to update manually via Firebase Console")
        
except Exception as e:
    print(f"✗ Error: {str(e)}")
    print("\nFallback: Update manually via Firebase Console")
    print("https://console.firebase.google.com/project/super-bowl-squares-fam-2026/database")
