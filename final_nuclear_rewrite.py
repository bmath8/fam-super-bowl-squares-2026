
import os
import re

path = r"c:\Users\mathe\OneDrive\Desktop\Fam Super Bowl Squares 2026\index.html"

# This script replaces the entire script block with a pure JS version.
# It preserves the constants and Firebase config but rewrites all components.

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Define the new script content
# Note: I will keep the existing constants and firebase config.
# I will only rewrite from "// Toast Component" down to the end of the script.

new_components = """
    // ── Toast Component (Pure JS) ─────────────────────────────────
    function Toast({ msg, onDone }) {
      const h = React.createElement;
      useEffect(() => { const t = setTimeout(onDone, 2500); return () => clearTimeout(t); }, []);
      return h('div', { className: "toast" }, msg);
    }

    // ── AvatarPicker (Pure JS) ────────────────────────────────────
    function AvatarPicker({ value, onChange, disabled, onClose }) {
      const h = React.createElement;
      return h('div', {
        style: { position: "fixed", inset: 0, zIndex: 999, background: "rgba(0,0,0,0.8)", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 },
        onClick: e => e.target === e.currentTarget && onClose && onClose()
      },
        h('div', { style: { background: "var(--card)", borderRadius: 16, padding: "20px 16px", maxWidth: 360, width: "100%", border: "1px solid var(--border2)", maxHeight: "70vh", overflowY: "auto" } },
          h('div', { className: "bebas", style: { fontSize: 18, letterSpacing: 2, color: "var(--gold)", marginBottom: 12, textAlign: "center" } }, "CHOOSE AVATAR"),
          h('div', { style: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(48px, 1fr))", gap: 8 } },
            AVATARS.map(a => h('button', {
              key: a,
              onClick: () => !disabled && onChange(a),
              disabled: disabled,
              style: {
                fontSize: 28, padding: 8, borderRadius: 10, border: "2px solid " + (value === a ? "var(--gold)" : "var(--border)"),
                background: value === a ? "var(--gold-glow)" : "var(--card)", cursor: disabled ? "default" : "pointer", opacity: disabled ? 0.5 : 1
              }
            }, a))
          )
        )
      );
    }

    // ── Pay Tab (Pure JS) ─────────────────────────────────────────
    function PayTab({ data, myName, dbr, toast }) {
      const h = React.createElement;
      const allNames = useMemo(() => [...new Set(safeGrid(data.grid).filter(Boolean) || [])], [data.grid]);
      const pps = data.pool?.pricePerSquare || 5;

      const togglePaid = (player) => {
        if (!dbr) return;
        const current = data.paidPlayers?.[player] || false;
        dbr.child("paidPlayers").child(player).set(!current);
        toast(player + (current ? " marked unpaid" : " marked paid"));
      };

      return h('div', { style: { padding: 16, animation: "fadeIn .3s ease" } },
        (data.zellePhone || data.zelleEmail) && h('div', { style: { background: "linear-gradient(135deg, var(--nav) 0%, #0a0f18 100%)", borderRadius: 16, padding: 20, marginBottom: 20, border: "1px solid var(--border2)", boxShadow: "0 10px 30px rgba(0,0,0,0.3)" } },
          h('div', { className: "bebas", style: { fontSize: 18, color: "var(--gold)", marginBottom: 12, letterSpacing: 1 } }, "PAYMENT INFO"),
          h('div', { style: { display: "flex", gap: 10 } },
            data.zellePhone && h('div', { style: { flex: 1, background: "rgba(0,0,0,0.2)", borderRadius: 10, padding: 10 } },
              h('div', { style: { fontSize: 9, fontWeight: 700, color: "var(--soft)", marginBottom: 4 } }, "PHONE"),
              h('div', { style: { fontSize: 14, fontWeight: 700, color: "#fff" } }, data.zellePhone),
              h('button', { onClick: () => { navigator.clipboard.writeText(data.zellePhone); toast("Copied!"); }, style: { marginTop: 6, width: "100%", padding: 6, borderRadius: 6, border: "none", background: "var(--gold)", color: "#000", fontSize: 11, fontWeight: 700 } }, "Copy")
            ),
            data.zelleEmail && h('div', { style: { flex: 1, background: "rgba(0,0,0,0.2)", borderRadius: 10, padding: 10 } },
              h('div', { style: { fontSize: 9, fontWeight: 700, color: "var(--soft)", marginBottom: 4 } }, "EMAIL"),
              h('div', { style: { fontSize: 13, fontWeight: 700, color: "#fff", wordBreak: "break-all" } }, data.zelleEmail),
              h('button', { onClick: () => { navigator.clipboard.writeText(data.zelleEmail); toast("Copied!"); }, style: { marginTop: 6, width: "100%", padding: 6, borderRadius: 6, border: "none", background: "var(--gold)", color: "#000", fontSize: 11, fontWeight: 700 } }, "Copy")
            )
          )
        ),
        allNames.length > 0 && h(React.Fragment, null,
          h('div', { className: "bebas", style: { fontSize: 16, color: "var(--gold)", marginBottom: 12 } }, "PAYMENT TRACKER"),
          allNames.map(name => {
            const ct = safeGrid(data.grid).filter(n => n === name).length;
            const owed = ct * pps;
            const paid = data.paidPlayers?.[name] || false;
            return h('div', { key: name, onClick: () => togglePaid(name), style: { display: "flex", alignItems: "center", gap: 10, padding: "10px 12px", background: "var(--card)", borderRadius: 10, marginBottom: 4, border: "1px solid " + (paid ? "#22C55E33" : "var(--border)"), cursor: "pointer" } },
              h('span', { style: { fontSize: 18 } }, getPlayerEmoji(data.playerMeta, name)),
              h('div', { style: { flex: 1 } },
                h('div', { style: { fontSize: 13, fontWeight: 600 } }, name),
                h('div', { style: { fontSize: 11, color: "var(--soft)" } }, ct + " squares • $" + owed + " owed")
              ),
              h('div', { style: { padding: "4px 10px", borderRadius: 6, fontSize: 11, fontWeight: 700, background: paid ? "rgba(34,197,94,0.15)" : "rgba(239,68,68,0.15)", color: paid ? "#22C55E" : "#EF4444" } }, paid ? "✓ Paid" : "Unpaid")
            );
          })
        )
      );
    }

    // ── Chat Tab (Pure JS) ────────────────────────────────────────
    function ChatTab({ data, myName, dbr }) {
      const h = React.createElement;
      const [msg, setMsg] = useState("");
      const [sub, setSub] = useState("chat");
      const bottomRef = useRef(null);

      const send = () => {
        if (!msg.trim()) return;
        const chat = [...(data.chat || []), { who: myName, msg: msg.trim(), ts: Date.now() }].slice(-200);
        dbr.update({ chat });
        setMsg("");
        playSound("chat");
      };

      useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [data.chat, data.feed]);
      const feed = useMemo(() => [...(data.feed || [])].reverse(), [data.feed]);

      return h('div', { style: { padding: 16, animation: "fadeIn .3s ease", display: "flex", flexDirection: "column", minHeight: "calc(100vh - 180px)" } },
        h('div', { style: { display: "flex", gap: 4, marginBottom: 12, background: "var(--card)", borderRadius: 10, padding: 3 } },
          [["chat", "💬 Chat"], ["activity", "📋 Activity"]].map(([k, l]) => h('button', {
            key: k,
            onClick: () => setSub(k),
            style: { flex: 1, padding: 8, borderRadius: 8, border: "none", fontSize: 12, fontWeight: 600, background: sub === k ? "var(--accent)" : "transparent", color: sub === k ? "#fff" : "var(--soft)" }
          }, l))
        ),
        sub === "chat" ? h(React.Fragment, null,
          h('div', { style: { flex: 1, overflowY: "auto", marginBottom: 12 } },
            (data.chat || []).length === 0 ? h('div', { style: { textAlign: "center", padding: 40, color: "var(--faint)" } }, h('div', { style: { fontSize: 32, marginBottom: 8 } }, "💬"), h('div', { style: { fontSize: 13 } }, "No messages yet.")) :
            (data.chat || []).map((m, i) => h('div', { key: i, style: { marginBottom: 8, display: "flex", flexDirection: m.who === myName ? "row-reverse" : "row", gap: 8, alignItems: "flex-start" } },
              h('div', { style: { fontSize: 20, width: 32, height: 32, borderRadius: "50%", background: getPlayerColor(m.who, [...new Set((data.chat || []).map(c => c.who))]) + "22", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 } }, getPlayerEmoji(data.playerMeta, m.who)),
              h('div', { style: { maxWidth: "75%" } },
                h('div', { style: { fontSize: 10, color: "var(--soft)", marginBottom: 2, textAlign: m.who === myName ? "right" : "left" } }, m.who),
                h('div', { style: { padding: "8px 12px", borderRadius: 12, fontSize: 13, background: m.who === myName ? "var(--accent)" : "var(--card)", color: m.who === myName ? "#fff" : "var(--text)", border: "1px solid " + (m.who === myName ? "transparent" : "var(--border)") } }, m.msg),
                h('div', { style: { fontSize: 9, color: "var(--faint)", marginTop: 2, textAlign: m.who === myName ? "right" : "left" } }, new Date(m.ts).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" }))
              )
            )),
            h('div', { ref: bottomRef })
          ),
          h('div', { style: { display: "flex", gap: 8 } },
            h('input', { value: msg, onChange: e => setMsg(e.target.value), placeholder: "Trash talk...", onKeyDown: e => e.key === "Enter" && send(), style: { flex: 1, padding: "10px 14px", borderRadius: 12, border: "1px solid var(--border2)", background: "var(--input)", color: "var(--text)", fontSize: 14 } }),
            h('button', { onClick: send, style: { padding: "10px 20px", borderRadius: 12, border: "none", background: "var(--accent)", color: "#fff", fontSize: 13, fontWeight: 700 } }, "Send")
          )
        ) : h('div', { style: { flex: 1, overflowY: "auto" } },
          feed.length === 0 ? h('div', { style: { textAlign: "center", padding: 40, color: "var(--faint)" } }, h('div', { style: { fontSize: 32, marginBottom: 8 } }, "📋"), h('div', { style: { fontSize: 13 } }, "No activity yet")) :
          feed.map((f, i) => h('div', { key: i, style: { padding: "10px 12px", borderRadius: 10, background: "var(--card)", marginBottom: 4, border: "1px solid var(--border)", display: "flex", justifyContent: "space-between", alignItems: "center" } },
            h('div', { style: { fontSize: 12, color: "var(--text)" } }, h('span', { style: { fontWeight: 700 } }, f.who), " " + f.msg),
            h('div', { style: { fontSize: 10, color: "var(--faint)" } }, new Date(f.ts).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" }))
          ))
        )
      );
    }

    // ── Props Tab (Pure JS) ───────────────────────────────────────
    function PropsTab({ data, myName, dbr, toast }) {
      const h = React.createElement;
      const [sub, setSub] = useState("picks");
      const [viewedPlayer, setViewedPlayer] = useState(null);
      const myPicks = (data.props && data.props[myName]) || {};

      const pickProp = (id, val) => {
         if (data.playerMeta?.[myName]?.confirmed) return toast("Locked!");
         if (!dbr) return;
         dbr.child("props").child(myName).child(id).set(val);
         playSound("claim");
      };

      const leaderboard = useMemo(() => {
        if (!data.props || !data.propAnswers) return [];
        return Object.keys(data.props).map(name => {
          let pts = 0;
          PROPS_LIST.forEach(p => { if (data.props[name][p.id] && data.props[name][p.id] === data.propAnswers[p.id]) pts++; });
          return [name, pts];
        }).sort((a,b) => b[1] - a[1]);
      }, [data.props, data.propAnswers]);

      return h('div', { style: { padding: 16, animation: "fadeIn .3s ease" } },
        h('div', { style: { display: "flex", gap: 8, marginBottom: 16 } },
          h('button', { onClick: () => setSub("picks"), style: { flex: 1, padding: 8, borderRadius: 8, background: sub === "picks" ? "var(--gold)" : "var(--card)", color: sub === "picks" ? "#000" : "#fff", border: "none", fontWeight: 700 } }, "My Picks"),
          h('button', { onClick: () => setSub("results"), style: { flex: 1, padding: 8, borderRadius: 8, background: sub === "results" ? "var(--gold)" : "var(--card)", color: sub === "results" ? "#000" : "#fff", border: "none", fontWeight: 700 } }, "Leaderboard")
        ),
        sub === "picks" ? h('div', null, PROPS_LIST.map(p => {
          const pick = myPicks[p.id];
          const ans = data.propAnswers?.[p.id];
          return h('div', { key: p.id, style: { background: "var(--card)", padding: 12, borderRadius: 12, marginBottom: 8, border: "1px solid var(--border)" } },
            h('div', { style: { fontSize: 13, marginBottom: 8 } }, p.q),
            h('div', { style: { display: "flex", gap: 4 } }, p.opts.map(o => h('button', {
              key: o, onClick: () => pickProp(p.id, o),
              style: { flex: 1, padding: 8, borderRadius: 6, border: "none", background: pick === o ? "var(--gold)" : "var(--card2)", color: pick === o ? "#000" : "#fff", fontSize: 11, fontWeight: 700 }
            }, o)))
          );
        })) : 
        h('div', null, leaderboard.map(([name, pts], i) => h('div', { key: name, style: { padding: 12, background: "var(--card)", borderRadius: 10, marginBottom: 4, display: "flex", justifyContent: "space-between" } }, h('span', null, (i + 1) + ". " + name), h('span', { className: "bebas" }, pts + "/" + PROPS_LIST.length))))
      );
    }

    // ── SettingsModal (Pure JS) ───────────────────────────────────
    function SettingsModal({ data, dbr, onClose, toast, toggleTheme, isDark, onShowAvatarPicker, isHost }) {
      const h = React.createElement;
      const [pin, setPin] = useState("");
      const [showPin, setShowPin] = useState(!data.hostPin);

      const needsPin = data.hostPin && !showPin;
      const checkPin = () => (pin === data.hostPin) ? (setShowPin(true), toast("Unlocked")) : toast("Wrong PIN");

      const unlockBoard = () => dbr?.update({ isLocked: false, colNums: null, rowNums: null });
      const resetBoard = () => confirm("Reset board?") && dbr?.update({ ...DEFAULT });

      if (needsPin) return h('div', { style: { position: "fixed", inset: 0, zIndex: 999, background: "rgba(0,0,0,0.8)", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 } },
        h('div', { style: { background: "var(--card)", borderRadius: 16, padding: 24, maxWidth: 340, width: "100%" } },
          h('div', { className: "bebas", style: { color: "var(--gold)", marginBottom: 16 } }, "HOST PIN"),
          h('input', { type: "password", value: pin, onChange: e => setPin(e.target.value), style: { width: "100%", padding: 12, background: "var(--input)", color: "#fff", marginBottom: 12 } }),
          h('button', { onClick: checkPin, style: { width: "100%", padding: 12, background: "var(--gold)" } }, "Enter")
        )
      );

      return h('div', { style: { position: "fixed", inset: 0, zIndex: 999, background: "rgba(0,0,0,0.8)", display: "flex", alignItems: "flex-end" }, onClick: e => e.target === e.currentTarget && onClose() },
        h('div', { style: { background: "var(--bg)", width: "100%", padding: 20, borderRadius: "20px 20px 0 0", maxHeight: "80vh", overflowY: "auto" } },
          h('div', { style: { display: "flex", justifyContent: "space-between", marginBottom: 20 } },
            h('div', { className: "bebas", style: { fontSize: 22, color: "var(--gold)" } }, "SETTINGS"),
            h('button', { className: "toggle-switch " + (isDark ? "on" : ""), onClick: toggleTheme })
          ),
          h('button', { onClick: onShowAvatarPicker, style: { width: "100%", padding: 12, marginBottom: 20 } }, "Change Avatar"),
          isHost && h('div', null,
            h('button', { onClick: () => dbr.child("isLocked").set(!data.isLocked), style: { width: "100%", padding: 12, background: data.isLocked ? "red" : "green", color: "#fff", marginBottom: 10 } }, data.isLocked ? "UNLOCK BOARD" : "LOCK BOARD"),
            h('div', { style: { padding: 10, background: "var(--card)", marginBottom: 10 } },
               h('label', null, "Price per square: "),
               h('input', { type: "number", value: data.pool?.pricePerSquare, onChange: e => dbr.child("pool/pricePerSquare").set(Number(e.target.value)) })
            ),
            h('button', { onClick: resetBoard, style: { width: "100%", padding: 10, background: "#333", color: "red" } }, "RESET BOARD")
          ),
          h('button', { onClick: onClose, style: { width: "100%", padding: 12, marginTop: 10 } }, "Close")
        )
      );
    }

    // ── Modals (Pure JS) ──────────────────────────────────────────
    function ShareModal({ data, room, onClose, toast }) {
      const h = React.createElement;
      const url = window.location.origin + window.location.pathname + "?room=" + room;
      const copy = () => { navigator.clipboard.writeText(url); toast("Link copied!"); onClose(); };
      return h('div', { style: { position: "fixed", inset: 0, zIndex: 999, background: "rgba(0,0,0,0.8)", display: "flex", alignItems: "center", justifyContent: "center" }, onClick: e => e.target === e.currentTarget && onClose() },
        h('div', { style: { background: "var(--card)", padding: 24, borderRadius: 16 } },
          h('div', { className: "bebas", style: { color: "var(--gold)", fontSize: 20, marginBottom: 16 } }, "SHARE GAME"),
          h('div', { style: { background: "var(--input)", padding: 12, marginBottom: 16, fontSize: 24, textAlign: "center" } }, room),
          h('button', { onClick: copy, style: { width: "100%", padding: 12, background: "var(--gold)" } }, "Copy Link")
        )
      );
    }

    function RulesModal({ data, onClose }) { 
      const h = React.createElement;
      return h('div', { style: { position: "fixed", inset: 0, zIndex: 999, background: "rgba(0,0,0,0.8)", display: "flex", alignItems: "flex-end" }, onClick: onClose }, 
        h('div', { style: { background: "var(--card)", padding: 24, borderRadius: "20px 20px 0 0", width: "100%" } },
          h('div', { className: "bebas", style: { fontSize: 22, color: "var(--gold)", marginBottom: 16 } }, "HOW TO PLAY"),
          h('div', { style: { fontSize: 13, color: "var(--text)" } }, "Tap empty squares to claim. Numbers assigned at kickoff. Winners Intersect!"),
          h('button', { onClick: onClose, style: { width: "100%", padding: 12, marginTop: 20 } }, "Got it!")
        )
      );
    }

    function WinnerModal({ data, onClose }) {
      const h = React.createElement;
      return h('div', { style: { position: "fixed", inset: 0, zIndex: 2000, background: "rgba(0,0,0,0.9)", display: "flex", alignItems: "center", justifyContent: "center" }, onClick: onClose },
        h('div', { style: { background: "var(--card)", padding: 30, borderRadius: 16, border: "2px solid var(--gold)", textAlign: "center" } },
          h('div', { style: { fontSize: 40 } }, "🏆"),
          h('div', { className: "bebas", style: { color: "var(--gold)", fontSize: 24, margin: "10px 0" } }, "WINNERS CIRCLE"),
          h('button', { onClick: onClose, style: { background: "var(--gold)", border: "none", padding: "10px 20px" } }, "Awesome!")
        )
      );
    }

    function NeedToWinModal({ data, myName, onClose }) {
      const h = React.createElement;
      const mySquares = [];
      if (data.colNums && data.rowNums) {
        data.grid.forEach((row, r) => row.forEach((cell, c) => { if (cell === myName) mySquares.push({ sea: data.colNums[c], ne: data.rowNums[r] }); }));
      }
      return h('div', { style: { position: "fixed", inset: 0, zIndex: 2000, background: "rgba(0,0,0,0.85)", display: "flex", alignItems: "center", justifyContent: "center" }, onClick: onClose },
        h('div', { style: { background: "var(--card)", padding: 24, borderRadius: 16, width: "90%", maxWidth: 360 } },
          h('div', { className: "bebas", style: { textAlign: "center", marginBottom: 16 } }, "MY WINNING NUMBERS"),
          h('div', { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 } },
            mySquares.map((s, i) => h('div', { key: i, style: { background: "var(--input)", padding: 10, textAlign: "center" } }, "SEA " + s.sea + " - NE " + s.ne))
          ),
          h('button', { onClick: onClose, style: { width: "100%", padding: 12, marginTop: 20 } }, "Close")
        )
      );
    }

    function OnboardingModal({ onClose }) {
      const h = React.createElement;
      return h('div', { style: { position: "fixed", inset: 0, zIndex: 3000, background: "rgba(0,0,0,0.9)", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 } },
        h('div', { style: { background: "var(--card)", padding: 24, borderRadius: 16, border: "1px solid var(--gold)" } },
          h('div', { style: { textAlign: "center", fontSize: 40 } }, "🏈"),
          h('div', { className: "bebas", style: { fontSize: 24, textAlign: "center", color: "var(--gold)" } }, "HOW TO PLAY"),
          h('p', { style: { margin: "20px 0" } }, "1. Pick Squares. 2. Numbers assigned at kickoff. 3. Win prizes!"),
          h('button', { onClick: onClose, style: { width: "100%", padding: 12, background: "var(--gold)" } }, "LET'S GO!")
        )
      );
    }

    function ConfirmPicksModal({ myName, data, onConfirm, onClose }) {
      const h = React.createElement;
      const [mode, setMode] = useState("money");
      return h('div', { style: { position: "fixed", inset: 0, zIndex: 3000, background: "rgba(0,0,0,0.9)", display: "flex", alignItems: "center", justifyContent: "center" } },
        h('div', { style: { background: "var(--card)", padding: 24, borderRadius: 16, width: 340 } },
          h('div', { className: "bebas", style: { color: "var(--gold)", textAlign: "center", marginBottom: 20 } }, "LOCK IN PICKS"),
          h('button', { onClick: () => setMode("money"), style: { width: "100%", padding: 16, marginBottom: 10, border: mode === "money" ? "2px solid gold" : "none" } }, "💵 PLAY FOR MONEY"),
          h('button', { onClick: () => setMode("fun"), style: { width: "100%", padding: 16, marginBottom: 20, border: mode === "fun" ? "2px solid gold" : "none" } }, "🆓 PLAY FOR FUN"),
          h('button', { onClick: () => onConfirm(mode), style: { width: "100%", padding: 16, background: "var(--gold)" } }, "CONFIRM"),
          h('button', { onClick: onClose, style: { width: "100%", padding: 10, marginTop: 10 } }, "Cancel")
        )
      );
    }

    // ── Main App (Pure JS) ────────────────────────────────────────
    function App() {
      const h = React.createElement;
      const [myName, setMyName] = useState(() => localStorage.getItem("sbName") || "");
      const [room, setRoom] = useState(() => new URLSearchParams(window.location.search).get("room") || "");
      const [joined, setJoined] = useState(false);
      const [showOnboarding, setShowOnboarding] = useState(() => !localStorage.getItem("onboarded"));
      const [data, setData] = useState(DEFAULT);
      const [isDark, setIsDark] = useState(() => localStorage.getItem("theme") !== "light");
      const [tab, setTab] = useState("board");
      const [toastMsg, setToastMsg] = useState(null);
      const [showSettings, setShowSettings] = useState(false);
      const [showShare, setShowShare] = useState(false);
      const [showRules, setShowRules] = useState(false);
      const [showWin, setShowWin] = useState(false);
      const [showNeed, setShowNeed] = useState(false);
      const [avatar, setAvatar] = useState(null);
      const [showAvatarPicker, setShowAvatarPicker] = useState(false);
      const [isHost, setIsHost] = useState(false);
      const dbrRef = useRef(null);

      const toast = useCallback((msg) => { setToastMsg(msg); }, []);

      const join = useCallback((name, rm) => {
        const playerId = getPlayerId(name);
        setMyName(name); setRoom(rm); localStorage.setItem("sbName", name);
        const ref = dbRef(rm); dbrRef.current = ref;

        const url = new URL(window.location); url.searchParams.set("room", rm); window.history.replaceState({}, "", url);

        ref.on("value", snap => {
          const val = snap.val();
          if (val) {
            let grid = Array.from({ length: 10 }, () => Array(10).fill(null));
            if (val.grid) {
              for (let r = 0; r < 10; r++) {
                 const row = val.grid[r] || val.grid[String(r)];
                 if (row) for (let c = 0; c < 10; c++) grid[r][c] = row[c] || row[String(c)] || null;
              }
            }
            setData({ ...DEFAULT, ...val, grid });
          } else {
            ref.set({ ...DEFAULT, hostCreator: playerId });
            setIsHost(true); localStorage.setItem("sbHost_" + rm, "true");
          }
        });

        ref.child("hostCreator").once("value", snap => {
           if (snap.val() === playerId || localStorage.getItem("sbHost_" + rm) === "true") setIsHost(true);
        });

        ref.child("playerMeta").child(name).once("value", snap => {
          const meta = snap.val();
          if (!meta) {
            const a = AVATARS[Math.floor(Math.random() * AVATARS.length)];
            ref.child("playerMeta").child(name).set({ avatar: a, joinedAt: Date.now(), playerId });
            setAvatar(a);
          } else {
            setAvatar(meta.avatar);
          }
        });

        requestNotificationPermission();
        setJoined(true);
      }, []);

      const dbr = dbrRef.current;

      useEffect(() => {
        if (isDark) document.body.classList.remove("light-theme");
        else document.body.classList.add("light-theme");
        localStorage.setItem("theme", isDark ? "dark" : "light");
      }, [isDark]);

      const [showConfirmModal, setShowConfirmModal] = useState(false);
      const confirmPicks = (mode) => {
        dbr?.child("playerMeta").child(myName).update({ confirmed: true, playMode: mode, lockedAt: Date.now() });
        setShowConfirmModal(false); toast("Locked In!"); playSound("lock");
      };

      const TABS = [
        { id: "board", icon: "🏈", label: "Board" },
        { id: "scores", icon: "📊", label: "Scores" },
        { id: "props", icon: "🎯", label: "Props" },
        { id: "chat", icon: "💬", label: "Chat" },
        { id: "pay", icon: "💰", label: "Pay" }
      ];

      if (!joined) return h(SetupScreen, { onJoin: join });

      return h('div', { style: { minHeight: "100vh", background: "var(--bg)" } },
        toastMsg && h(Toast, { msg: toastMsg, onDone: () => setToastMsg(null) }),
        showSettings && h(SettingsModal, { data, dbr, isHost, isDark, toggleTheme: () => setIsDark(!isDark), onClose: () => setShowSettings(false), toast, onShowAvatarPicker: () => { setShowSettings(false); setShowAvatarPicker(true); } }),
        showOnboarding && h(OnboardingModal, { onClose: () => { setShowOnboarding(false); localStorage.setItem("onboarded", "true"); } }),
        showShare && h(ShareModal, { data, room, onClose: () => setShowShare(false), toast }),
        showRules && h(RulesModal, { data, onClose: () => setShowRules(false) }),
        showWin && h(WinnerModal, { data, onClose: () => setShowWin(false) }),
        showNeed && h(NeedToWinModal, { data, myName, onClose: () => setShowNeed(false) }),
        showConfirmModal && h(ConfirmPicksModal, { myName, data, onClose: () => setShowConfirmModal(false), onConfirm: confirmPicks }),
        showAvatarPicker && h(AvatarPicker, { value: avatar, onChange: (a) => { setAvatar(a); dbr?.child("playerMeta").child(myName).child("avatar").set(a); setShowAvatarPicker(false); }, onClose: () => setShowAvatarPicker(false) }),

        h(GameHeader, { data, myName }),

        h('div', { style: { display: "flex", gap: 5, padding: "6px 10px", justifyContent: "center" } },
           h('button', { onClick: () => setShowAvatarPicker(true), style: { padding: "5px 10px", borderRadius: 8, border: "1px solid var(--border2)", background: "var(--card)" } }, h('span', null, avatar), " ", myName),
           h('button', { onClick: () => setShowShare(true), style: { padding: "5px 10px", borderRadius: 8, border: "1px solid var(--border2)", background: "var(--card)" } }, "Share"),
           h('button', { onClick: () => setShowSettings(true), style: { padding: "5px 10px", borderRadius: 8, border: "1px solid var(--border2)", background: "var(--card)" } }, "⚙"),
           h('button', { onClick: () => setShowRules(true), style: { padding: "5px 10px", borderRadius: 8, border: "1px solid var(--border2)", background: "var(--card)" } }, "📋")
        ),

        h('div', { style: { paddingBottom: 80 } },
           tab === "board" && h(BoardTab, { data, myName, dbr, toast }),
           tab === "scores" && h(ScoresTab, { data, dbr, toast }),
           tab === "props" && h(PropsTab, { data, myName, dbr, toast }),
           tab === "chat" && h(ChatTab, { data, myName, dbr }),
           tab === "pay" && h(PayTab, { data, myName, dbr, toast })
        ),

        h('div', { className: "bottom-nav" }, TABS.map(t => h('button', { key: t.id, className: "nav-btn " + (tab === t.id ? "active" : ""), onClick: () => setTab(t.id) }, h('span', { className: "nav-icon" }, t.icon), h('span', null, t.label), h('span', { className: "nav-dot" })))),

        !data.playerMeta?.[myName]?.confirmed && (safeGrid(data.grid).includes(myName)) && h('div', { style: { position: "fixed", bottom: 80, left: 0, right: 0, padding: 10 } },
           h('button', { onClick: () => setShowConfirmModal(true), style: { width: "100%", padding: 16, background: "var(--gold)", fontWeight: 800, borderRadius: 12 } }, "LOCK IN PICKS")
        )
      );
    }

    // ── Render ─────────────────────────────────────────────────────
    trace("React-Mounting");
    ReactDOM.createRoot(document.getElementById("root")).render(React.createElement(App));
"""

# Extract the part before Toast
end_comp = content.find("// ── Toast Component")
if end_comp == -1:
     # Fallback: maybe Toast isn't there yet, look for whatever was after useGameStatus
     end_comp = content.find("function SetupScreen")

# We want to keep everything from start of script till the components start
# But SetupScreen is ALREADY pure JS, and GameHeader too.
# Let's find the first place where we want to start replacing everything.

# Actually, to be super safe, I'll replace everything from line 707 (Toast) to the end of script.
# Wait, I also need to make sure I don't delete SetupScreen, GameHeader, BoardTab, ScoresTab
# which are ALREADY pure JS.

# Let's see where they are.
# SetupScreen starts at 764.
# GameHeader starts after SetupScreen.
# BoardTab starts after GameHeader.
# ScoresTab starts after BoardTab.

# I'll replace from line 1400 (PayTab start was around there) up to the end.
# Wait, let's find the actual start of PayTab.
start_pay = content.find("function PayTab")
if start_pay == -1:
     # Maybe it's missing or named differently
     start_pay = content.find("${tab === 'pay'") # Look for usage

# I'll just look for "function PayTab"
start_pay_match = re.search(r'function PayTab', content)
if start_pay_match:
    start_idx = start_pay_match.start()
    # Find the end of the script
    end_idx = content.rfind("</script>")
    
    print(f"Replacing from {start_idx} to {end_idx}")
    content = content[:start_idx] + new_components + "\n  " + content[end_idx:]
else:
    print("Could not find PayTab")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Finished final_nuclear_rewrite.")
