# Setting Final Score: SEA 29 - NE 13

## ⚡ Quick Option: Use Firebase Console (FASTEST)

1. Go to [Firebase Console](https://console.firebase.google.com/project/super-bowl-squares-fam-2026/database/super-bowl-squares-fam-2026-default-rtdb/data)
2. Find your pool node (usually under `/pools/`)
3. Click on `scores` and edit:
   - Click **SEA** → Edit the array values for each quarter
   - Click **NE** → Edit the array values for each quarter
4. Click on `gameMeta` and set:
   - `status`: `"STATUS_FINAL"`
   - `period`: `4`
   - `seaTotal`: `29`
   - `neTotal`: `13`
   - `clock`: `"0:00"`
   - `detail`: `"Final"`

## 📝 What You Need to Know

**You need the quarter-by-quarter breakdown!**

For total SEA 29 - NE 13, you need to know what each quarter was, for example:
- Q1: SEA 3, NE 0
- Q2: SEA 6, NE 0  
- Q3: SEA 13, NE 7
- Q4: SEA 7, NE 6

**In Firebase, you'd set:**
```
scores/SEA: [3, 6, 13, 7]
scores/NE: [0, 0, 7, 6]
```

## 🔧 Option 2: Via the App

Since auto-sync is now disabled:
1. Hard refresh the app (Ctrl+F5)
2. Go to **Scores** tab (you need to be host)
3. Manually enter each quarter's score
4. They will now persist!

## ✅ Once Set

After setting the final score:
- Refresh the app
- Verify the board shows correct winners
- Check that payouts are calculated correctly
- Winners should be highlighted with gold badges

**Do you know the quarter-by-quarter breakdown?** I can help you format it correctly for Firebase!
