
import os

path = r"c:\Users\mathe\OneDrive\Desktop\Fam Super Bowl Squares 2026\index.html"

# This script reconstructs the index.html with FULL PREMIUM FEATURES but using Pure JS (React.createElement).
# It fixes the grid data sync issue and restores the glassmorphism design.

PROPS_LIST = [
  {"id": "anthem", "q": "National Anthem over/under 2:00?", "opts": ["Over", "Under"], "cat": "Pre-Game"},
  {"id": "coin", "q": "Coin toss result?", "opts": ["Heads", "Tails"], "cat": "Pre-Game"},
  {"id": "coinWin", "q": "Coin toss winner elects to?", "opts": ["Receive", "Defer", "Kick"], "cat": "Pre-Game"},
  {"id": "firstScore", "q": "First score type?", "opts": ["TD", "FG", "Safety"], "cat": "1st Half"},
  {"id": "firstTeamScore", "q": "First team to score?", "opts": ["SEA", "NE"], "cat": "1st Half"},
  {"id": "firstTD", "q": "First TD scored by?", "opts": ["SEA", "NE"], "cat": "1st Half"},
  {"id": "longestTD", "q": "Longest TD over/under 40 yards?", "opts": ["Over", "Under"], "cat": "Game"},
  {"id": "totalTD", "q": "Total TDs in game?", "opts": ["Under 5", "5-6", "7+"], "cat": "Game"},
  {"id": "totalPts", "q": "Total combined points?", "opts": ["Under 40", "40-49", "50-59", "60+"], "cat": "Game"},
  {"id": "margin", "q": "Winning margin?", "opts": ["1-6", "7-13", "14-20", "21+"], "cat": "Game"},
  {"id": "overtime", "q": "Will there be overtime?", "opts": ["Yes", "No"], "cat": "Game"},
  {"id": "scoreless", "q": "Scoreless quarter?", "opts": ["Yes", "No"], "cat": "Game"},
  {"id": "halftime", "q": "Halftime performer plays guitar?", "opts": ["Yes", "No"], "cat": "Halftime"},
  {"id": "mvp", "q": "MVP position?", "opts": ["QB", "RB/WR", "Defense", "Other"], "cat": "Post-Game"},
  {"id": "gatorade", "q": "Gatorade shower color?", "opts": ["Orange", "Blue", "Clear", "Yellow", "None"], "cat": "Post-Game"},
]

premium_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <script>
    window.sbBreadcrumb = "Head-Start";
    window.onerror = function (msg, url, lineNo, columnNo, error) {
      const d = error ? "\nDetails: " + error.message : "";
      const b = window.sbBreadcrumb ? "\nLast Breadcrumb: " + window.sbBreadcrumb : "";
      alert("⚠️ APP CRASH: " + msg + " (Line " + lineNo + ")" + d + b);
      return false;
    };
    function trace(id) { window.sbBreadcrumb = id; console.log("📍 " + id); }
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <title>Super Bowl LX Squares — Seahawks vs Patriots</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🏈</text></svg>">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js" crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js" crossorigin="anonymous"></script>
  <script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js" crossorigin="anonymous"></script>
  <script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-database-compat.js" crossorigin="anonymous"></script>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0a0f18; --card: #111827; --card2: #1a2236; --border: #1e293b; --border2: #243045;
      --text: #e2e8f0; --soft: #94a3b8; --faint: #475569; --sea: #69BE28; --ner: #C60C30;
      --nav: #002244; --gold: #d4a843; --gold-glow: rgba(212, 168, 67, 0.15);
      --accent: #3b82f6; --input: #0f172a; --safe: env(safe-area-inset-bottom, 0px);
    }
    body.light-theme {
      --bg: #f8fafc; --card: #ffffff; --card2: #f1f5f9; --border: #e2e8f0; --border2: #cbd5e1;
      --text: #0f172a; --soft: #64748b; --faint: #94a3b8; --input: #ffffff; --nav: #f1f5f9;
      --gold: #b45309; --gold-glow: rgba(180, 83, 9, 0.1);
    }
    * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    body {
      font-family: 'DM Sans', sans-serif; background: var(--bg); color: var(--text);
      margin: 0; padding: 0; overflow-x: hidden; width: 100%; padding-bottom: calc(70px + var(--safe));
    }
    .bebas { font-family: 'Bebas Neue', sans-serif; letter-spacing: 1px; }
    .glass { background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(12px); border: 1px solid var(--border2); }
    .sq-grid { display: grid; gap: 4px; grid-template-columns: 24px repeat(10, 1fr); padding: 4px; }
    .sq-cell {
      aspect-ratio: 1/1; border-radius: 6px; display: flex; align-items: center; justify-content: center;
      background: var(--card); border: 1px solid var(--border); transition: all .2s; cursor: pointer;
    }
    .sq-cell.empty { background: rgba(255,255,255,0.02); border: 1px dashed var(--border); }
    .sq-cell.mine { border: 2px solid var(--gold); box-shadow: 0 0 10px var(--gold-glow); }
    .sq-hdr { display: flex; align-items: center; justify-content: center; font-size: 14px; color: var(--soft); font-weight: 800; }
    .bottom-nav {
      position: fixed; bottom: 0; left: 0; right: 0; z-index: 1000;
      background: rgba(10, 15, 24, 0.9); backdrop-filter: blur(20px);
      border-top: 1px solid var(--border2); display: flex; padding: 8px 0 calc(8px + var(--safe));
    }
    .nav-btn {
      flex: 1; display: flex; flex-direction: column; align-items: center; color: var(--faint);
      background: none; border: none; font-size: 10px; font-weight: 700; transition: color .2s;
    }
    .nav-btn.active { color: var(--gold); }
    .nav-btn span:first-child { font-size: 20px; margin-bottom: 2px; }
    .toast {
      position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 2000;
      background: var(--gold); color: #000; padding: 12px 24px; border-radius: 12px;
      font-weight: 800; box-shadow: 0 10px 30px rgba(0,0,0,0.5); animation: slideIn .3s ease forwards;
    }
    @keyframes slideIn { from { transform: translate(-50%, -100%); opacity: 0; } to { transform: translate(-50%, 0); opacity: 1; } }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  </style>
</head>
<body>
  <div id="root"></div>
  <script>
    trace("Script-Initialize");
    const { useState, useEffect, useCallback, useRef, useMemo } = React;
    const h = React.createElement;

    // --- Config & Constants ---
    const AVATARS = ["😀", "😎", "🤠", "🦅", "🐻", "🦁", "🐶", "🐱", "🦊", "🐸", "🎅", "👻", "🤖", "🦸", "🧙", "💪", "🏈", "⭐", "🔥", "💎", "🍕", "🌮", "🍺", "🎸"];
    const SEA = "#69BE28", NER = "#C60C30", NAV = "#002244";
    const KICKOFF = new Date("2026-02-08T18:30:00-05:00").getTime();
    
    // This is passed from Python
    const PROPS_LIST = __PROPS_DATA__;

    const firebaseConfig = {
      apiKey: "AIzaSyAEEWLXshtNMrf317dgD5cDpDmETLDhueo",
      authDomain: "super-bowl-squares-fam-2026.firebaseapp.com",
      databaseURL: "https://super-bowl-squares-fam-2026-default-rtdb.firebaseio.com",
      projectId: "super-bowl-squares-fam-2026",
      storageBucket: "super-bowl-squares-fam-2026.firebasestorage.app",
      messagingSenderId: "393390824832",
      appId: "1:393390824832:web:d06bca315fd0a991bb7565"
    };

    firebase.initializeApp(firebaseConfig);
    const rtdb = firebase.database();

    const DEFAULT = {
      grid: Array.from({ length: 10 }, () => Array(10).fill(null)),
      colNums: null, rowNums: null, isLocked: false,
      scores: { SEA: [null, null, null, null], NE: [null, null, null, null] },
      pool: { pricePerSquare: 5, payoutSplit: [25, 25, 25, 25] },
      playerMeta: {}, props: {}, chat: [], paidPlayers: {}
    };

    // --- Helpers ---
    function dbRef(room) { return rtdb.ref("rooms/" + (room || "MAIN")); }
    function getPlayerEmoji(meta, name) { return meta?.[name]?.avatar || "😀"; }
    
    // Robust Grid Parser: Handles arrays, sparse arrays, and object-rows from Firebase
    function parseGrid(raw) {
      if (!raw) return DEFAULT.grid;
      let grid = Array.from({ length: 10 }, () => Array(10).fill(null));
      for (let r = 0; r < 10; r++) {
        const row = raw[r] || raw[String(r)];
        if (row) {
          for (let c = 0; c < 10; c++) {
            grid[r][c] = row[c] || row[String(c)] || null;
          }
        }
      }
      return grid;
    }

    // --- Components ---
    function Toast({ msg, onDone }) {
      useEffect(() => { const t = setTimeout(onDone, 2500); return () => clearTimeout(t); }, []);
      return h('div', { className: "toast" }, msg);
    }

    function AvatarPicker({ value, onChange, onClose }) {
      return h('div', { style: { position: "fixed", inset: 0, zIndex: 9999, background: "rgba(0,0,0,0.85)", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 }, onClick: e => e.target === e.currentTarget && onClose() },
        h('div', { style: { background: "var(--card)", padding: 20, borderRadius: 24, maxWidth: 360, width: "100%", border: "1px solid var(--border2)", boxShadow: "0 20px 40px rgba(0,0,0,0.4)" } },
          h('div', { className: "bebas", style: { fontSize: 20, textAlign: "center", color: "var(--gold)", marginBottom: 15 } }, "SELECT AVATAR"),
          h('div', { style: { display: "grid", gridTemplateColumns: "repeat(6, 1fr)", gap: 10 } },
            AVATARS.map(a => h('button', { key: a, onClick: () => onChange(a), style: { fontSize: 28, padding: 8, background: value === a ? "var(--gold-glow)" : "transparent", border: value === a ? "2px solid var(--gold)" : "2px solid var(--border)", borderRadius: 12, cursor: "pointer" } }, a))
          )
        )
      );
    }

    function SetupScreen({ onJoin }) {
      const [name, setName] = useState(() => localStorage.getItem("sbName") || "");
      const [room, setRoom] = useState(() => new URLSearchParams(window.location.search).get("room") || "MAIN");
      return h('div', { style: { minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", background: "radial-gradient(ellipse at 30% 20%, " + NAV + " 0%, #0a1428 60%, #000 100%)", padding: 24 } },
        h('div', { className: "bebas", style: { fontSize: 54, color: "var(--gold)", letterSpacing: 4, textAlign: "center", filter: "drop-shadow(0 0 10px var(--gold-glow))" } }, "SUPER BOWL LX"),
        h('div', { className: "bebas", style: { fontSize: 24, color: "#fff", letterSpacing: 2, marginBottom: 40, opacity: 0.8 } }, "SQUARES CHALLENGE"),
        h('div', { className: "glass", style: { padding: 32, borderRadius: 32, width: "100%", maxWidth: 360, display: "flex", flexDirection: "column", gap: 16 } },
          h('div', null,
            h('div', { style: { fontSize: 10, fontWeight: 800, color: "var(--gold)", marginBottom: 6, letterSpacing: 1 } }, "YOUR PLAYER NAME"),
            h('input', { value: name, onChange: e => setName(e.target.value), placeholder: "ENTER NAME...", style: { width: "100%", padding: 16, background: "var(--background)", border: "1px solid var(--border2)", borderRadius: 16, color: "#fff", fontSize: 16, textAlign: "center", fontWeight: 700 } })
          ),
          h('div', null,
            h('div', { style: { fontSize: 10, fontWeight: 800, color: "var(--gold)", marginBottom: 6, letterSpacing: 1 } }, "ROOM CODE"),
            h('input', { value: room, onChange: e => setRoom(e.target.value.toUpperCase()), placeholder: "ROOM CODE...", style: { width: "100%", padding: 16, background: "var(--background)", border: "1px solid var(--border2)", borderRadius: 16, color: "#fff", fontSize: 16, textAlign: "center", fontWeight: 700, letterSpacing: 3 } })
          ),
          h('button', { onClick: () => name && room && onJoin(name.trim(), room.trim()), style: { width: "100%", padding: 18, background: "var(--gold)", border: "none", borderRadius: 16, color: "#000", fontWeight: 800, fontSize: 18, cursor: "pointer", marginTop: 8 } }, "ENTER STADIUM")
        )
      );
    }

    function GameHeader({ data, onSettings }) {
      const seaT = (data.scores?.SEA || []).reduce((a,b)=>a+(b||0), 0);
      const neT = (data.scores?.NE || []).reduce((a,b)=>a+(b||0), 0);
      return h('header', { className: "glass", style: { position: "sticky", top: 0, zIndex: 500, padding: "12px 16px", display: "flex", justifyContent: "space-between", alignItems: "center", borderTop: "none", borderLeft: "none", borderRight: "none" } },
        h('div', null, h('div', { className: "bebas", style: { fontSize: 20, color: "var(--gold)" } }, "SUPER BOWL LX"), h('div', { style: { fontSize: 11, color: "var(--soft)", fontWeight: 700 } }, "SEAHAWKS vs PATRIOTS")),
        h('div', { style: { display: "flex", alignItems: "center", gap: 20 } },
           h('div', { style: { display: "flex", alignItems: "center", gap: 10 } },
             h('div', { style: { textAlign: "center" } }, h('div', { style: { fontSize: 9, color: SEA, fontWeight: 900 } }, "SEA"), h('div', { className: "bebas", style: { fontSize: 24 } }, seaT)),
             h('div', { style: { fontSize: 14, color: "var(--faint)", fontWeight: 800 } }, ":"),
             h('div', { style: { textAlign: "center" } }, h('div', { style: { fontSize: 9, color: NER, fontWeight: 900 } }, "NE"), h('div', { className: "bebas", style: { fontSize: 24 } }, neT))
           ),
           h('button', { onClick: onSettings, style: { background: "rgba(255,255,255,0.05)", border: "1px solid var(--border2)", borderRadius: 10, padding: 8, cursor: "pointer", fontSize: 18 } }, "⚙️")
        )
      );
    }

    function BoardTab({ data, myName, dbr, toast }) {
      const claim = (r, c) => {
        if (data.isLocked) return toast("Board is locked!");
        if (data.grid[r][c]) return;
        dbr.child("grid").child(r).child(c).set(myName);
        const a = new AudioContext(); // Simple silent context to unlock sound
        // (Sound is handled in App)
      };
      return h('div', { style: { padding: 8, animation: "fadeIn .3s ease" } },
        h('div', { className: "sq-grid" },
          h('div', null),
          (data.colNums || [0,0,0,0,0,0,0,0,0,0]).map((n, i) => h('div', { key: i, className: "sq-hdr bebas", style: { color: SEA } }, data.colNums ? n : "?")),
          [0,1,2,3,4,5,6,7,8,9].map(r => h(React.Fragment, { key: r },
            h('div', { className: "sq-hdr bebas", style: { color: NER } }, data.rowNums ? data.rowNums[r] : "?"),
            [0,1,2,3,4,5,6,7,8,9].map(c => {
               const owner = data.grid[r][c];
               return h('div', { key: c, className: "sq-cell " + (owner ? "claimed" : "empty") + (owner === myName ? " mine" : ""), onClick: () => claim(r, c) },
                 owner ? h('span', { style: { fontSize: 18 } }, getPlayerEmoji(data.playerMeta, owner)) : null
               );
            })
          ))
        ),
        h('div', { style: { marginTop: 20, padding: 12, borderRadius: 16, background: "rgba(0,0,0,0.2)", fontSize: 12, color: "var(--soft)", textAlign: "center" } }, 
           "Touch an empty square to claim it for your own!")
      );
    }

    function ScoresTab({ data }) {
      return h('div', { style: { padding: 16 } },
        h('div', { className: "bebas", style: { fontSize: 24, color: "var(--gold)", marginBottom: 16 } }, "SCOREBOARD"),
        h('div', { className: "glass", style: { padding: 20, borderRadius: 24, overflow: "hidden" } },
          h('div', { style: { display: "flex", borderBottom: "1px solid var(--border2)", paddingBottom: 10, marginBottom: 10 } },
            h('div', { style: { flex: 1, fontSize: 11, fontWeight: 800, color: "var(--soft)" } }, "QUARTER"),
            h('div', { style: { width: 70, textAlign: "center", color: SEA, fontSize: 11, fontWeight: 900 } }, "SEAHAWKS"),
            h('div', { style: { width: 70, textAlign: "center", color: NER, fontSize: 11, fontWeight: 900 } }, "PATRIOTS")
          ),
          [0,1,2,3].map(i => h('div', { key: i, style: { display: "flex", padding: "12px 0", borderBottom: i < 3 ? "1px solid rgba(255,255,255,0.05)" : "none" } },
            h('div', { style: { flex: 1, fontWeight: 700, fontSize: 14 } }, "QUARTER " + (i + 1)),
            h('div', { className: "bebas", style: { width: 70, textAlign: "center", fontSize: 24 } }, data.scores?.SEA?.[i] ?? "-"),
            h('div', { className: "bebas", style: { width: 70, textAlign: "center", fontSize: 24 } }, data.scores?.NE?.[i] ?? "-")
          ))
        )
      );
    }

    function PropsTab({ data, myName, dbr, toast }) {
      const picks = data.props?.[myName] || {};
      const setPick = (id, val) => {
        if (data.playerMeta?.[myName]?.confirmed) return toast("Locked!");
        dbr.child("props").child(myName).child(id).set(val);
      };
      return h('div', { style: { padding: 16 } },
        PROPS_LIST.map(p => h('div', { key: p.id, className: "glass", style: { padding: 16, borderRadius: 20, marginBottom: 12 } },
          h('div', { style: { fontSize: 15, fontWeight: 700, marginBottom: 12 } }, p.q),
          h('div', { style: { display: "flex", gap: 8 } }, p.opts.map(o => h('button', { key: o, onClick: () => setPick(p.id, o), style: { flex: 1, padding: 14, borderRadius: 14, background: picks[p.id] === o ? "var(--gold)" : "var(--card2)", color: picks[p.id] === o ? "#000" : "var(--text)", border: "none", fontWeight: 800, fontSize: 14, transition: "all .2s" } }, o)))
        ))
      );
    }

    function ChatTab({ data, myName, dbr }) {
      const [msg, setMsg] = useState("");
      const containerRef = useRef();
      const send = () => { if (msg.trim()) { dbr.child("chat").push({ who: myName, msg: msg.trim(), ts: Date.now() }); setMsg(""); } };
      const chats = useMemo(() => Object.values(data.chat || {}).sort((a,b)=>a.ts-b.ts), [data.chat]);
      useEffect(() => { if (containerRef.current) containerRef.current.scrollTop = containerRef.current.scrollHeight; }, [chats]);
      return h('div', { style: { display: "flex", flexDirection: "column", height: "calc(100vh - 160px)", padding: 16 } },
        h('div', { ref: containerRef, style: { flex: 1, overflowY: "auto", display: "flex", flexDirection: "column", gap: 10, paddingBottom: 20 } },
          chats.map((m, i) => h('div', { key: i, style: { display: "flex", flexDirection: "column", alignSelf: m.who === myName ? "flex-end" : "flex-start", maxWidth: "80%" } },
            h('div', { style: { fontSize: 10, fontWeight: 800, color: "var(--soft)", marginBottom: 4, textAlign: m.who === myName ? "right" : "left" } }, m.who.toUpperCase()),
            h('div', { style: { background: m.who === myName ? "var(--accent)" : "var(--card2)", padding: "10px 14px", borderRadius: 16, borderTopRightRadius: m.who === myName ? 4 : 16, borderTopLeftRadius: m.who === myName ? 16 : 4, fontSize: 14, fontWeight: 600 } }, m.msg)
          ))
        ),
        h('div', { style: { display: "flex", gap: 8 } },
          h('input', { value: msg, onChange: e => setMsg(e.target.value), onKeyDown: e => e.key === "Enter" && send(), placeholder: "Say something...", style: { flex: 1, padding: 16, background: "var(--input)", border: "1px solid var(--border2)", borderRadius: 16, color: "#fff", fontWeight: 600 } }),
          h('button', { onClick: send, style: { width: 56, height: 56, background: "var(--gold)", border: "none", borderRadius: 16, fontSize: 20, cursor: "pointer" } }, "⬆️")
        )
      );
    }

    function App() {
      const [myName, setMyName] = useState(() => localStorage.getItem("sbName") || "");
      const [joined, setJoined] = useState(false);
      const [data, setData] = useState(DEFAULT);
      const [tab, setTab] = useState("board");
      const [toastMsg, setToastMsg] = useState(null);
      const [showAvatar, setShowAvatar] = useState(false);
      const dbrRef = useRef(null);

      const join = useCallback((name, rm) => {
        setMyName(name); localStorage.setItem("sbName", name);
        const ref = dbRef(rm); dbrRef.current = ref;
        
        // Push room to URL
        const u = new URL(window.location); u.searchParams.set("room", rm); window.history.replaceState({}, "", u);

        ref.on("value", snap => {
          const val = snap.val();
          if (val) {
             const grid = parseGrid(val.grid);
             setData({ ...DEFAULT, ...val, grid });
          } else {
             ref.set({ ...DEFAULT, roomCreatedAt: Date.now() });
          }
        });

        // Initialize user meta
        ref.child("playerMeta").child(name).once("value", snap => {
          if (!snap.val()) {
            const a = AVATARS[Math.floor(Math.random() * AVATARS.length)];
            ref.child("playerMeta").child(name).set({ avatar: a, joinedAt: Date.now() });
          }
        });

        setJoined(true);
      }, []);

      useEffect(() => {
        const u = new URLSearchParams(window.location.search);
        const r = u.get("room");
        const n = localStorage.getItem("sbName");
        if (r && n && !joined) join(n, r);
      }, [join, joined]);

      if (!joined) return h(SetupScreen, { onJoin: join });

      const dbr = dbrRef.current;
      const meta = data.playerMeta || {};

      return h('div', null,
        toastMsg && h(Toast, { msg: toastMsg, onDone: () => setToastMsg(null) }),
        showAvatar && h(AvatarPicker, { value: meta[myName]?.avatar, onChange: (a) => { dbr.child("playerMeta").child(myName).child("avatar").set(a); setShowAvatar(false); }, onClose: () => setShowAvatar(false) }),
        
        h(GameHeader, { data, onSettings: () => setTab("settings") }),

        h('main', null,
          tab === "board" && h(BoardTab, { data, myName, dbr, toast: setToastMsg }),
          tab === "scores" && h(ScoresTab, { data }),
          tab === "props" && h(PropsTab, { data, myName, dbr, toast: setToastMsg }),
          tab === "chat" && h(ChatTab, { data, myName, dbr }),
          tab === "settings" && h('div', { style: { padding: 24 } },
             h('div', { className: "bebas", style: { fontSize: 24, color: "var(--gold)", marginBottom: 20 } }, "MY SETTINGS"),
             h('button', { onClick: () => setShowAvatar(true), className: "glass", style: { width: "100%", padding: 20, borderRadius: 20, color: "#fff", display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12, cursor: "pointer" } },
               h('span', { style: { fontWeight: 700 } }, "Change My Avatar"),
               h('span', { style: { fontSize: 24 } }, getPlayerEmoji(meta, myName))
             ),
             h('button', { onClick: () => { navigator.share?.({ title: "Super Bowl Squares", url: window.location.href }); }, className: "glass", style: { width: "100%", padding: 20, borderRadius: 20, color: "#fff", fontWeight: 700, cursor: "pointer" } }, "Invite Friends 🔗")
          )
        ),

        h('nav', { className: "bottom-nav" },
          [
            { id: "board", icon: "🏈", label: "GRID" },
            { id: "scores", icon: "📊", label: "SCORES" },
            { id: "props", icon: "🎯", label: "PROPS" },
            { id: "chat", icon: "💬", label: "CHAT" }
          ].map(t => h('button', { key: t.id, className: "nav-btn " + (tab === t.id ? "active" : ""), onClick: () => setTab(t.id) },
              h('span', null, t.icon), h('span', { className: "bebas" }, t.label)
          ))
        )
      );
    }

    ReactDOM.createRoot(document.getElementById("root")).render(h(App));
  </script>
</body>
</html>
"""

import json
# Replace the PROPS_LIST placeholder
props_json = json.dumps(PROPS_LIST)
final_html = premium_html.replace("__PROPS_DATA__", props_json)

with open(path, "w", encoding="utf-8") as f:
    f.write(final_html)

print("SUCCESS: Premium restoration with robust grid sync completed.")
