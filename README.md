# 🏈 Super Bowl Squares — Family Edition

A single-file, real-time Super Bowl squares + prop-bet web app. Built to run a live family
pool during the game: a 10×10 grid, randomized number assignment, automatic quarter-by-quarter
winner highlighting, live score sync, a prop-bet sheet, a chat feed, payouts, and a host/admin
console — all in one `index.html` (no build step).

## Stack
- **Frontend:** React (UMD) + `htm` tagged templates — zero build, runs from a single file
- **Realtime backend:** Firebase Realtime Database (live grid + scores + chat across devices)
- **State:** optimistic UI, live listeners, host-only write controls, security write-lock

## 🎮 Live demo (public build)
This repo ships in **DEMO_MODE** (`index.html`, top of the app script → `const DEMO_MODE = true`).
The demo is **fully self-contained**: it loads a pre-filled example board (grid, final score,
chat feed, props) entirely in the browser — **no backend, no keys, no data leaves the page.**
Just open `index.html` or host it as a static file.

## 🔌 Running it live (real pool)
1. Create your own Firebase project → Realtime Database.
2. Set `const DEMO_MODE = false`.
3. Provide config via a `window.SBSQ_ENV` object (e.g. a small `env.js` you don't commit):
   ```html
   <script>window.SBSQ_ENV = { FIREBASE_API_KEY: "…", FIREBASE_AUTH_DOMAIN: "…",
     FIREBASE_DB_URL: "…", FIREBASE_PROJECT_ID: "…", FIREBASE_STORAGE_BUCKET: "…",
     FIREBASE_SENDER_ID: "…", FIREBASE_APP_ID: "…" };</script>
   ```
No secrets are committed to this repo — the public build carries only placeholders.

## Highlights
- 10×10 grid with randomized, lockable number assignment
- Automatic per-quarter winner detection + payout math
- Live prop-bet sheet and reactions
- Host/admin console with a hard write-lock for post-game read-only mode
- Deployed via Netlify (`netlify.toml` included)
