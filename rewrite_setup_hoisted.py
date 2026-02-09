
import os
import re

path = r"c:\Users\mathe\OneDrive\Desktop\Fam Super Bowl Squares 2026\index.html"

# We will generate the SetupScreen code cleanly in Python and replace it.
# This prevents invisible char issues and ensures clean syntax.

setup_screen_code = """    // ── Setup Screen (Style Hoisted) ──────────────────────────────
    function SetupScreen({ onJoin }) {
      const [name, setName] = useState(() => localStorage.getItem("sbName") || "");
      const [room, setRoom] = useState(() => new URLSearchParams(window.location.search).get("room") || "MAIN");
      const cd = useCountdown();

      const go = () => {
        const n = name.trim();
        if (!n) return;
        localStorage.setItem("sbName", n);
        onJoin(n, room.trim().toUpperCase() || "MAIN");
      };

      // Hoisted Styles
      const containerStyle = {
        minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
        background: "radial-gradient(ellipse at 30% 20%, " + NAV + " 0%, #0a0f18 60%, #10060a 100%)",
        padding: "24px", position: "relative", overflow: "hidden"
      };
      
      const bgStyle1 = { position: "absolute", top: "-20%", left: "-10%", width: "60%", height: "60%", background: "radial-gradient(circle, rgba(105,190,40,0.08) 0%, transparent 70%)", pointerEvents: "none" };
      const bgStyle2 = { position: "absolute", bottom: "-20%", right: "-10%", width: "60%", height: "60%", background: "radial-gradient(circle, rgba(198,12,48,0.08) 0%, transparent 70%)", pointerEvents: "none" };
      
      const contentWrapperStyle = { position: "relative", zIndex: 1, textAlign: "center", animation: "fadeIn .6s ease" };
      
      const timerContainerStyle = { marginBottom: 24, display: "flex", gap: 8, justifyContent: "center" };
      
      const timerBoxStyle = { background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8, padding: "8px 12px", minWidth: 48 };
      
      const timerValStyle = { fontSize: 28, lineHeight: 1, color: "var(--text)" };
      const timerLabelStyle = { fontSize: 9, color: "var(--soft)", letterSpacing: 2, marginTop: 2 };
      
      const dateStyle = { fontSize: 11, letterSpacing: 6, color: "var(--soft)", marginBottom: 4, fontWeight: 600 };
      const titleStyle = { fontSize: "clamp(36px,10vw,56px)", lineHeight: 0.95, margin: "4px 0 16px", letterSpacing: 2, color: "#fff" };
      const lxStyle = { color: "var(--gold)" };
      
      const matchupContainerStyle = { display: "flex", alignItems: "center", justifyContent: "center", gap: 20, marginBottom: 32 };
      const teamBoxStyle = { textAlign: "center" };
      const logoStyle = (color) => ({ width: 64, height: 64, objectFit: "contain", filter: "drop-shadow(0 0 10px " + color + "66)" });
      const teamNameStyle = (color) => ({ fontSize: 14, color: color, marginTop: 6, letterSpacing: 2 });
      const vsStyle = { fontSize: 20, color: "var(--faint)" };
      
      const formBoxStyle = { background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 16, padding: "24px", maxWidth: 340, margin: "0 auto" };
      const labelStyle = { fontSize: 10, fontWeight: 700, letterSpacing: 2, color: "var(--soft)", display: "block", textAlign: "left", marginBottom: 6 };
      const inputStyle = { width: "100%", padding: "12px 14px", borderRadius: 10, border: "1px solid var(--border2)", background: "var(--input)", color: "var(--text)", fontSize: 16, fontWeight: 600, marginBottom: 16 };
      const inputRoomStyle = { ...inputStyle, marginBottom: 20, letterSpacing: 3 };
      
      const btnStyle = {
        width: "100%", padding: "14px", borderRadius: 12, border: "none",
        background: "linear-gradient(135deg, var(--gold) 0%, #C4983A 100%)",
        color: "#1a1a1a", fontSize: 15, fontWeight: 800, letterSpacing: 1,
        boxShadow: "0 4px 20px rgba(212,168,67,0.3)"
      };

      return React.createElement('div', { style: containerStyle },
        html`
          <div style=${bgStyle1} />
          <div style=${bgStyle2} />

          <div style=${contentWrapperStyle}>
            ${cd && html`
              <div style=${timerContainerStyle}>
                ${[["D", cd.d], ["H", cd.h], ["M", cd.m], ["S", cd.s]].map(([l, v]) => html`
                  <div key=${l} style=${timerBoxStyle}>
                    <div className="bebas" style=${timerValStyle}>${String(v).padStart(2, "0")}</div>
                    <div style=${timerLabelStyle}>${l}</div>
                  </div>
                `)}
              </div>
            `}

            <div style=${dateStyle}>FEB 8 • 2026</div>
            <h1 className="bebas" style=${titleStyle}>
              SUPER BOWL <span style=${lxStyle}>LX</span>
            </h1>

            <div style=${matchupContainerStyle}>
              <div style=${teamBoxStyle}>
                <img src="https://a.espncdn.com/i/teamlogos/nfl/500/sea.png" style=${logoStyle(SEA)} alt="SEA" />
                <div className="bebas" style=${teamNameStyle(SEA)}>SEAHAWKS</div>
              </div>
              <div className="bebas" style=${vsStyle}>VS</div>
              <div style=${teamBoxStyle}>
                <img src="https://a.espncdn.com/i/teamlogos/nfl/500/ne.png" style=${logoStyle(NER)} alt="NE" />
                <div className="bebas" style=${teamNameStyle(NER)}>PATRIOTS</div>
              </div>
            </div>

            <div style=${formBoxStyle}>
              <label style=${labelStyle}>YOUR NAME</label>
              <input value=${name} onChange=${e => setName(e.target.value)} placeholder="Enter your name"
                onKeyDown=${e => e.key === "Enter" && go()}
                style=${inputStyle} />

              <label style=${labelStyle}>ROOM CODE</label>
              <input value=${room} onChange=${e => setRoom(e.target.value.toUpperCase())} placeholder="MAIN"
                style=${inputRoomStyle} />

              <button onClick=${go} style=${btnStyle}>ENTER GAME →</button>
            </div>
          </div>
        `
      );
    }
"""

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "function SetupScreen" in line:
        start_idx = i
        break

if start_idx != -1:
    for i in range(start_idx, len(lines)):
        if "function GameHeader" in lines[i]:
            end_idx = i
            # Adjust to include/exclude comments or spacing as needed
            if i > 0 and "Compact Header" in lines[i-1]:
                end_idx = i - 1
            break

if start_idx != -1 and end_idx != -1:
    del lines[start_idx:end_idx]
    lines.insert(start_idx, setup_screen_code + "\n\n")
    
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Rewrote SetupScreen with hoisted styles.")
else:
    print(f"Could not find range: {start_idx} to {end_idx}")
