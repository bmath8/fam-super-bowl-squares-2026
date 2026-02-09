import requests
import json

# Firebase REST API endpoint
DATABASE_URL = "https://super-bowl-squares-fam-2026-default-rtdb.firebaseio.com"

print("🔍 Checking Firebase database structure...")
print("=" * 60)

# Get the entire database root to see the structure
try:
    response = requests.get(f"{DATABASE_URL}.json?shallow=true")
    root_structure = response.json()
    
    print("Database root keys:")
    if root_structure:
        for key in root_structure.keys():
            print(f"  - {key}")
            
        # Try to find the actual data path
        # Common paths: direct root, pools/, pool/, data/, etc.
        paths_to_try = [
            "",  # Direct root
            "pools",
            "pool", 
            "data",
            "game"
        ]
        
        found_path = None
        for path in paths_to_try:
            test_url = f"{DATABASE_URL}/{path}.json" if path else f"{DATABASE_URL}.json"
            test_response = requests.get(test_url)
            test_data = test_response.json()
            
            if test_data and isinstance(test_data, dict):
                if 'scores' in test_data or any('scores' in str(v) for v in (test_data.values() if isinstance(test_data, dict) else [])):
                    found_path = path
                    print(f"\n✓ Found scores data at path: {'root' if not path else path}")
                    print(f"  Structure: {list(test_data.keys())[:10]}")  # Show first 10 keys
                    break
        
        if found_path is not None:
            # Final scores
            final_scores = {
                "SEA": [3, 9, 7, 10],
                "NE": [0, 0, 0, 13]
            }
            
            game_meta = {
                "status": "STATUS_FINAL",
                "period": 4,
                "clock": "0:00",
                "detail": "Final",
                "seaTotal": 29,
                "neTotal": 13
            }
            
            update_path = f"{DATABASE_URL}/{found_path}" if found_path else DATABASE_URL
            
            print(f"\n📊 Updating scores at: {update_path}")
            
            # Update scores
            scores_response = requests.patch(
                f"{update_path}/scores.json",
                data=json.dumps(final_scores)
            )
            
            print(f"Scores update: {scores_response.status_code}")
            if scores_response.status_code == 200:
                print("✓ Scores updated!")
                
            # Update metadata
            meta_response = requests.patch(
                f"{update_path}/gameMeta.json",
                data=json.dumps(game_meta)
            )
            
            print(f"Metadata update: {meta_response.status_code}")
            if meta_response.status_code == 200:
                print("✓ Metadata updated!")
                
            print("\n✅ UPDATE COMPLETE!")
            print(f"Final Score: SEA 29 - NE 13")
        else:
            print("\n⚠️  Could not auto-locate scores path")
            print("Please update manually via Firebase Console")
            
    else:
        print("  Database appears empty or inaccessible")
        
except Exception as e:
    print(f"✗ Error: {str(e)}")
    
print("\n" + "=" * 60)
