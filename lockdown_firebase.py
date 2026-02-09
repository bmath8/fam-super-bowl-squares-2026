import requests
import json

DB_URL = "https://super-bowl-squares-fam-2026-default-rtdb.firebaseio.com"

print("🔒 LOCKING DOWN FIREBASE SECURITY")
print("=" * 70)

# Set database rules to READ-ONLY
rules = {
    "rules": {
        ".read": True,   # Anyone can read (view final results)
        ".write": False  # NO ONE can write (completely locked)
    }
}

try:
    # Update Firebase security rules via REST API
    response = requests.put(
        f"{DB_URL}/.settings/rules.json",
        json=rules
    )
    
    if response.status_code == 200:
        print("✅ FIREBASE LOCKED TO READ-ONLY")
        print("\nSecurity Status:")
        print("  ✓ All users can VIEW final results")
        print("  ✓ NO ONE can modify data (including you)")
        print("  ✓ Scores are permanently frozen")
        print("  ✓ Database is safe from tampering")
        print("\n🔐 Database is now secure until next year!")
    else:
        print(f"⚠️  Rule update status: {response.status_code}")
        print("\nMANUAL STEPS REQUIRED:")
        print("1. Go to: https://console.firebase.google.com/")
        print("2. Select: super-bowl-squares-fam-2026")
        print("3. Click: Realtime Database → Rules")
        print("4. Replace with:")
        print(json.dumps(rules, indent=2))
        print("5. Click: Publish")
        
except Exception as e:
    print(f"⚠️  Automated update failed: {e}")
    print("\nMANUAL LOCKDOWN REQUIRED:")
    print("-" * 70)
    print("Go to Firebase Console and set these rules:")
    print(json.dumps(rules, indent=2))

print("=" * 70)
