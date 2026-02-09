
import os

path = r"c:\Users\mathe\OneDrive\Desktop\Fam Super Bowl Squares 2026\index.html"

# Master Clean Slate Script
# This script identifies the body script tag and replaces its entire contents with a single, clean, pure-JS version.

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Identify the script tag in the body.
# It starts after <div id="root"></div>
body_start_marker = '<div id="root"></div>'
start_idx = content.find(body_start_marker)
if start_idx == -1:
     raise Exception("Could not find root div")

script_start = content.find("<script>", start_idx)
script_end = content.find("</script>", script_start)

if script_start == -1 or script_end == -1:
     raise Exception("Could not find script tag in body")

# 2. Reconstruct the entire script content
clean_script = r"""
    trace("Script-Initialize");
    const { useState, useEffect, useCallback, useRef, useMemo } = React;
    const h = React.createElement;

    /* ═══════════════════════════════════════════════════════════════
       SUPER BOWL LX SQUARES — CLEAN SLATE PURE JS VERSION
       Seahawks vs Patriots • Feb 8, 2026
       ═══════════════════════════════════════════════════════════════ */

    const SEA = "#69BE28", NER = "#C60C30", NAV = "#002244";
    const QS = ["Q1", "Q2", "Q3", "Q4"];
    const AVATARS = ["😀", "😎", "🤠", "🦅", "🐻", "🦁", "🐶", "🐱", "🦊", "🐸", "🎅", "👻", "🤖", "🦸", "🧙", "💪", "🏈", "⭐", "🔥", "💎", "🍕", "🌮", "🍺", "🎸"];
    const PROPS_LIST = [
      { id: "anthem", q: "National Anthem over/under 2:00?", opts: ["Over", "Under"], cat: "Pre-Game" },
      { id: "coin", q: "Coin toss result?", opts: ["Heads", "Tails"], cat: "Pre-Game" },
      { id: "coinWin", q: "Coin toss winner elects to?", opts: ["Receive", "Defer", "Kick"], cat: "Pre-Game" },
      { id: "firstScore", q: "First score type?", opts: ["TD", "FG", "Safety"], cat: "1st Half" },
      { id: "firstTeamScore", q: "First team to score?", opts: ["SEA", "NE"], cat: "1st Half" },
      { id: "firstTD", q: "First TD scored by?", opts: ["SEA", "NE"], cat: "1st Half" },
      { id: "longestTD", q: "Longest TD over/under 40 yards?", opts: ["Over", "Under"], cat: "Game" },
      { id: "totalTD", q: "Total TDs in game?", opts: ["Under 5", "5-6", "7+"], cat: "Game" },
      { id: "totalPts", q: "Total combined points?", opts: ["Under 40", "40-49", "50-59", "60+"], cat: "Game" },
      { id: "margin", q: "Winning margin?", opts: ["1-6", "7-13", "14-20", "21+"], cat: "Game" },
      { id: "overtime", q: "Will there be overtime?", opts: ["Yes", "No"], cat: "Game" },
      { id: "scoreless", q: "Scoreless quarter?", opts: ["Yes", "No"], cat: "Game" },
      { id: "halftime", q: "Halftime performer plays guitar?", opts: ["Yes", "No"], cat: "Halftime" },
      { id: "mvp", q: "MVP position?", opts: ["QB", "RB/WR", "Defense", "Other"], cat: "Post-Game" },
      { id: "gatorade", q: "Gatorade shower color?", opts: ["Orange", "Blue", "Clear", "Yellow", "None"], cat: "Post-Game" },
    ];
    const KICKOFF = new Date("2026-02-08T18:30:00-05:00").getTime();

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
      pool: { pricePerSquare: 5, payoutSplit: [25, 25, 25, 25], payoutPreset: "even", propBuyIn: 2 },
      settings: { maxPerPlayer: 0, showHeatMap: false },
      feed: [], playerMeta: {}, props: {}, propAnswers: {},
      hostPin: "", zellePhone: "", zelleEmail: "", darkMode: true,
      chat: [], paidPlayers: {},
    };

    function dbRef(room) { return rtdb.ref("rooms/" + (room || "MAIN")); }
    function getPlayerId(name) {
      const key = "sbPlayerId_" + name;
      let id = localStorage.getItem(key);
      if (!id) { id = name + "_" + Date.now().toString(36); localStorage.setItem(key, id); }
      return id;
    }

    function playSound(type) {
      try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const o = ctx.createOscillator(), g = ctx.createGain();
        o.connect(g); g.connect(ctx.destination);
        if (type === "claim") { o.frequency.value = 880; g.gain.value = 0.1; o.start(); o.stop(ctx.currentTime + 0.08); }
        else if (type === "win") { o.frequency.value = 523; g.gain.value = 0.15; o.start(); o.stop(ctx.currentTime + 0.4); }
        else if (type === "lock") { o.frequency.value = 440; g.gain.value = 0.1; o.start(); o.stop(ctx.currentTime + 0.2); }
      } catch (e) {}
    }

    function safeGrid(g) {
      if (!Array.isArray(g)) return [];
      return g.reduce((acc, row) => acc.concat(Array.isArray(row) ? row : (row && typeof row === "object" ? Object.values(row) : [])), []);
    }

    function getWinner(grid, colNums, rowNums, seaScore, neScore) {
      if (!colNums || !rowNums || seaScore == null || neScore == null) return null;
      const ci = colNums.indexOf(seaScore % 10), ri = rowNums.indexOf(neScore % 10);
      return (ci >= 0 && ri >= 0) ? grid[ri]?.[ci] : null;
    }

    function getPlayerEmoji(meta, name) { return meta?.[name]?.avatar || "😀"; }
    function getPlayerColor(name, allNames) {
      const palette = ["#69BE28", "#C60C30", "#3B82F6", "#D4A843", "#A855F7", "#EC4899", "#14B8A6", "#F97316"];
      return palette[allNames.indexOf(name) % palette.length];
    }

    function addFeed(data, name, msg) { return [...(data.feed || []), { who: name, msg, ts: Date.now() }].slice(-50); }

    function Toast({ msg, onDone }) {
      useEffect(() => { const t = setTimeout(onDone, 2500); return () => clearTimeout(t); }, []);
      return h('div', { className: "toast" }, msg);
    }

    function AvatarPicker({ value, onChange, onClose }) {
      return h('div', { style: { position: "fixed", inset: 0, zIndex: 9999, background: "rgba(0,0,0,0.85)", display: "flex", alignItems: "center", justifyContent: "center" }, onClick: e => e.target === e.currentTarget && onClose() },
        h('div', { style: { background: "var(--card)", padding: 20, borderRadius: 16, maxWidth: 350, border: "1px solid var(--border2)" } },
          h('div', { className: "bebas", style: { textAlign: "center", color: "var(--gold)", marginBottom: 15 } }, "SELECT AVATAR"),
          h('div', { style: { display: "grid", gridTemplateColumns: "repeat(6, 1fr)", gap: 8 } },
            AVATARS.map(a => h('button', { key: a, onClick: () => onChange(a), style: { fontSize: 24, padding: 8, background: value === a ? "var(--gold-glow)" : "transparent", border: value === a ? "1px solid var(--gold)" : "none", borderRadius: 8 } }, a))
          )
        )
      );
    }

    function useCountdown() {
      const [left, setLeft] = useState(KICKOFF - Date.now());
      useEffect(() => { const i = setInterval(() => setLeft(KICKOFF - Date.now()), 1000); return () => clearInterval(i); }, []);
      if (left <= 0) return null;
      return { d: Math.floor(left/86400000), h: Math.floor((left%86400000)/3600000), m: Math.floor((left%3600000)/60000), s: Math.floor((left%60000)/1000) };
    }

    function SetupScreen({ onJoin }) {
      const [name, setName] = useState(() => localStorage.getItem("sbName") || "");
      const [room, setRoom] = useState(() => new URLSearchParams(window.location.search).get("room") || "MAIN");
      const cd = useCountdown();
      return h('div', { style: { minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", background: "radial-gradient(ellipse at 30% 20%, " + NAV + " 0%, #0a0f18 60%, #10060a 100%)", padding: 24 } },
        h('div', { className: "bebas", style: { fontSize: 42, color: "var(--gold)", letterSpacing: 4, textAlign: "center", marginBottom: 10 } }, "SUPER BOWL LX"),
        h('div', { className: "bebas", style: { fontSize: 20, color: "#fff", letterSpacing: 2, marginBottom: 30 } }, "SQUARES CHALLENGE"),
        h('div', { style: { width: "100%", maxWidth: 320, background: "rgba(255,255,255,0.03)", backdropFilter: "blur(10px)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 24, padding: 24 } },
          h('input', { value: name, onChange: e => setName(e.target.value), placeholder: "YOUR NAME", style: { width: "100%", padding: 14, background: "#000", border: "1px solid #333", borderRadius: 12, color: "#fff", fontSize: 16, marginBottom: 12, textAlign: "center" } }),
          h('input', { value: room, onChange: e => setRoom(e.target.value.toUpperCase()), placeholder: "ROOM CODE", style: { width: "100%", padding: 14, background: "#000", border: "1px solid #333", borderRadius: 12, color: "#fff", fontSize: 16, marginBottom: 20, textAlign: "center" } }),
          h('button', { onClick: () => name && room && onJoin(name, room), style: { width: "100%", padding: 16, background: "var(--gold)", border: "none", borderRadius: 12, color: "#000", fontWeight: 800, fontSize: 16, letterSpacing: 1 } }, "JOIN GAME")
        ),
        cd && h('div', { style: { marginTop: 40, textAlign: "center" } }, h('div', { style: { fontSize: 11, color: "var(--soft)", letterSpacing: 2, marginBottom: 8 } }, "KICKOFF IN"), h('div', { className: "bebas", style: { fontSize: 24, color: "#fff" } }, cd.d + "D " + cd.h + "H " + cd.m + "M " + cd.s + "S"))
      );
    }

    function GameHeader({ data, myName }) {
      return h('div', { className: "header-bar", style: { background: "rgba(17,24,39,0.98)", borderBottom: "1px solid var(--border)", padding: "10px 16px", position: "sticky", top: 0, zIndex: 100, backdropFilter: "blur(16px)" } },
        h('div', { style: { display: "flex", justifyContent: "space-between", alignItems: "center" } },
          h('div', null, h('div', { className: "bebas", style: { fontSize: 18, color: "var(--gold)", letterSpacing: 1 } }, "SUPER BOWL LX"), h('div', { style: { fontSize: 10, color: "var(--soft)", fontWeight: 700 } }, "SEAHAWKS vs PATRIOTS")),
          h('div', { style: { textAlign: "right" } },
            h('div', { style: { display: "flex", gap: 12, alignItems: "center" } },
              h('div', { style: { textAlign: "center" } }, h('div', { style: { fontSize: 9, color: SEA, fontWeight: 800 } }, "SEA"), h('div', { className: "bebas", style: { fontSize: 20 } }, data.scores?.SEA?.filter(s=>s!=null).reduce((a,b)=>a+b,0) || 0)),
              h('div', { style: { fontSize: 14, color: "var(--faint)" } }, "vs"),
              h('div', { style: { textAlign: "center" } }, h('div', { style: { fontSize: 9, color: NER, fontWeight: 800 } }, "NE"), h('div', { className: "bebas", style: { fontSize: 20 } }, data.scores?.NE?.filter(s=>s!=null).reduce((a,b)=>a+b,0) || 0))
            )
          )
        )
      );
    }

    function BoardTab({ data, myName, dbr, toast }) {
      const claim = (r, c) => {
        if (data.isLocked) return toast("Board is locked!");
        if (data.grid[r][c]) return;
        dbr.child("grid").child(r).child(c).set(myName);
        playSound("claim");
      };
      return h('div', { style: { padding: 10, animation: "fadeIn .4s ease" } },
        h('div', { className: "sq-grid" },
          h('div', { className: "sq-hdr" }, ""),
          (data.colNums || [0,0,0,0,0,0,0,0,0,0]).map((n, i) => h('div', { key: i, className: "sq-hdr bebas", style: { color: SEA } }, data.colNums ? n : "?")),
          [0,1,2,3,4,5,6,7,8,9].map(r => h(React.Fragment, { key: r },
            h('div', { className: "sq-hdr bebas", style: { color: NER } }, data.rowNums ? data.rowNums[r] : "?"),
            [0,1,2,3,4,5,6,7,8,9].map(c => {
               const owner = data.grid[r][c];
               return h('div', { key: c, className: "sq-cell " + (owner ? "claimed" : "empty") + (owner === myName ? " mine" : ""), onClick: () => claim(r, c) },
                 owner ? h('span', { style: { fontSize: 14 } }, getPlayerEmoji(data.playerMeta, owner)) : null
               );
            })
          ))
        )
      );
    }

    function ScoresTab({ data }) {
      return h('div', { style: { padding: 16 } },
        h('div', { className: "bebas", style: { fontSize: 20, color: "var(--gold)", marginBottom: 15 } }, "SCOREBOARD"),
        h('div', { style: { background: "var(--card)", borderRadius: 12, padding: 16 } },
          h('div', { style: { display: "flex", marginBottom: 10 } },
            h('div', { style: { flex: 1, color: "var(--soft)", fontSize: 11 } }, "QUARTER"),
            h('div', { style: { width: 60, textAlign: "center", color: SEA, fontSize: 11, fontWeight: 800 } }, "SEA"),
            h('div', { style: { width: 60, textAlign: "center", color: NER, fontSize: 11, fontWeight: 800 } }, "NE")
          ),
          [0,1,2,3].map(i => h('div', { key: i, style: { display: "flex", padding: "8px 0", borderBottom: i < 3 ? "1px solid var(--border)" : "none" } },
            h('div', { style: { flex: 1, fontWeight: 700 } }, QS[i]),
            h('div', { className: "bebas", style: { width: 60, textAlign: "center" } }, data.scores?.SEA?.[i] ?? "-"),
            h('div', { className: "bebas", style: { width: 60, textAlign: "center" } }, data.scores?.NE?.[i] ?? "-")
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
        PROPS_LIST.map(p => h('div', { key: p.id, style: { background: "var(--card)", padding: 12, borderRadius: 12, marginBottom: 10 } },
          h('div', { style: { fontSize: 14, marginBottom: 10 } }, p.q),
          h('div', { style: { display: "flex", gap: 5 } }, p.opts.map(o => h('button', { key: o, onClick: () => setPick(p.id, o), style: { flex: 1, padding: 10, borderRadius: 8, background: picks[p.id] === o ? "var(--gold)" : "var(--card2)", color: picks[p.id] === o ? "#000" : "#fff", border: "none", fontWeight: 700 } }, o)))
        ))
      );
    }

    function ChatTab({ data, myName, dbr }) {
       const [msg, setMsg] = useState("");
       const send = () => { if (msg.trim()) { dbr.child("chat").push({ who: myName, msg, ts: Date.now() }); setMsg(""); } };
       return h('div', { style: { padding: 16, display: "flex", flexDirection: "column", height: "calc(100vh - 200px)" } },
         h('div', { style: { flex: 1, overflowY: "auto" } },
           Object.values(data.chat || {}).map((m, i) => h('div', { key: i, style: { marginBottom: 10 } }, h('span', { style: { fontWeight: 700, color: "var(--gold)" } }, m.who + ": "), h('span', null, m.msg)))
         ),
         h('div', { style: { display: "flex", gap: 5, marginTop: 10 } },
           h('input', { value: msg, onChange: e => setMsg(e.target.value), style: { flex: 1, padding: 10, background: "var(--input)", color: "#fff", border: "1px solid #333" } }),
           h('button', { onClick: send, style: { padding: "10px 20px", background: "var(--accent)", color: "#fff" } }, "SEND")
         )
       );
    }

    function PayTab({ data, toast }) {
       return h('div', { style: { padding: 20, textAlign: "center" } }, h('div', { className: "bebas", style: { fontSize: 24, color: "var(--gold)" } }, "PAYMENTS"), h('p', { style: { marginTop: 20, color: "var(--soft)" } }, "Host has not set up payment details yet."));
    }

    function App() {
      const [myName, setMyName] = useState(() => localStorage.getItem("sbName") || "");
      const [room, setRoom] = useState(() => new URLSearchParams(window.location.search).get("room") || "");
      const [joined, setJoined] = useState(false);
      const [data, setData] = useState(DEFAULT);
      const [tab, setTab] = useState("board");
      const [toastMsg, setToastMsg] = useState(null);
      const dbrRef = useRef(null);

      const join = (name, rm) => {
        setMyName(name); setRoom(rm); localStorage.setItem("sbName", name);
        const ref = dbRef(rm); dbrRef.current = ref;
        ref.on("value", snap => setData({ ...DEFAULT, ...snap.val() }));
        setJoined(true);
      };

      if (!joined) return h(SetupScreen, { onJoin: join });

      return h('div', { style: { minHeight: "100vh", background: "var(--bg)" } },
        toastMsg && h(Toast, { msg: toastMsg, onDone: () => setToastMsg(null) }),
        h(GameHeader, { data, myName }),
        h('div', { style: { paddingBottom: 80 } },
          tab === "board" && h(BoardTab, { data, myName, dbr: dbrRef.current, toast: (m) => setToastMsg(m) }),
          tab === "scores" && h(ScoresTab, { data }),
          tab === "props" && h(PropsTab, { data, myName, dbr: dbrRef.current, toast: (m) => setToastMsg(m) }),
          tab === "chat" && h(ChatTab, { data, myName, dbr: dbrRef.current }),
          tab === "pay" && h(PayTab, { data })
        ),
        h('div', { className: "bottom-nav" }, 
          [["board", "🏈", "Grid"], ["scores", "📊", "Scores"], ["props", "🎯", "Props"], ["chat", "💬", "Chat"], ["pay", "💰", "Pay"]].map(([id, icon, label]) => h('button', { key: id, className: "nav-btn " + (tab === id ? "active" : ""), onClick: () => setTab(id) }, h('span', { className: "nav-icon" }, icon), h('span', null, label)))
        )
      );
    }

    ReactDOM.createRoot(document.getElementById("root")).render(h(App));
"""

# 3. Assemble the new file content
new_content = content[:script_start + 8] + clean_script + "\n  " + content[script_end:]

with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("SUCCESS: total_cleansing_rewrite completed.")
