# 🏈 Super Bowl Squares — Real-Time Multiplayer Pool

A live, multiplayer **Super Bowl Squares** web app for running a family/friends pool. Players claim squares on a 10×10 grid and everyone's board updates **in real time**; winners are tracked automatically each quarter based on the score's last digits — with celebration animations when a square is claimed or wins.

Built for Super Bowl LX (Seahawks vs Patriots) and used by a real group on game day.

![Live Demo](https://img.shields.io/badge/demo-live-success)
![React](https://img.shields.io/badge/React-18-61DAFB)
![Firebase](https://img.shields.io/badge/Firebase-Realtime_DB-FFCA28)
![Zero build](https://img.shields.io/badge/deploy-single_file_static-informational)

> **Live demo:** _deploying — link coming here_

## Features

- **10×10 squares grid** with row/column digits assigned for the two teams.
- **Real-time sync** — claims and score updates propagate instantly to every connected device via Firebase Realtime Database (no refresh).
- **Claim flow** with name entry and animated feedback (pop / ripple / flash) when a square is taken.
- **Automatic quarter winners** — computed from the last digit of each team's score at the end of each quarter.
- **Live scoreboard** and payout tracking per quarter.
- **Admin controls** for setting/finalizing scores and managing the room.
- **Mobile-first** — designed to be used on phones during the game.

## Tech

- **React 18** (UMD, no build step) for the UI.
- **Firebase Realtime Database** for shared state + live multiplayer sync.
- Ships as a **single self-contained `index.html`** — all dependencies load from CDN, so it deploys as a static file anywhere (Vercel / Netlify / any static host).

## Run locally

Because it's a single static file, just open it:

```bash
# any static server, e.g.
npx serve .
# then open the printed localhost URL
```

Firebase config is embedded for the shared demo room; access to writes is restricted by Firebase security rules.

## Deploy

Static single-file deploy — no build required. On Vercel, the included `vercel.json` serves the repo root as static content. On Netlify, `netlify.toml` does the same.

## Notes

This was a real, ship-it-for-game-day project. The board reflects the completed Super Bowl LX pool, so the live demo shows a finished game end-to-end.
