
import os
import re

path = r"c:\Users\mathe\OneDrive\Desktop\Fam Super Bowl Squares 2026\index.html"

# Pure JS GameHeader
new_game_header = """    // ── GameHeader (Pure JS) ──────────────────────────────────────
    function GameHeader({ data, myName }) {
      const h = React.createElement;
      const { status, cd } = useGameStatus(data);
      const totalSea = (data.scores?.SEA || []).reduce((a, b) => a + (b || 0), 0);
      const totalNe = (data.scores?.NE || []).reduce((a, b) => a + (b || 0), 0);
      const claimed = safeGrid(data.grid).filter(Boolean).length || 0;
      const pot = claimed * (data.pool?.pricePerSquare || 0);

      const headerStyle = {
        background: "linear-gradient(180deg, rgba(17,24,39,0.98) 0%, rgba(10,15,24,0.95) 100%)",
        borderBottom: "1px solid var(--border)",
        padding: "8px 16px 6px", position: "sticky", top: 0, zIndex: 100,
        backdropFilter: "blur(16px)"
      };

      const rowStyle = { display: "flex", alignItems: "center", justifyContent: "center", gap: 0 };
      const teamLeftStyle = { flex: 1, display: "flex", alignItems: "center", gap: 6 };
      const teamRightStyle = { flex: 1, display: "flex", alignItems: "center", justifyContent: "flex-end", gap: 6 };
      const logoStyle = { width: 32, height: 32, flexShrink: 0, objectFit: "contain" };
      const centerStyle = { textAlign: "center", padding: "0 10px", minWidth: 70 };
      
      const teamLabelStyle = (color) => ({ fontSize: 12, color: color, letterSpacing: 2, lineHeight: 1 });
      const scoreStyle = { fontSize: 22, lineHeight: 1, color: "#fff" };

      const progBarStyle = { height: 3, background: "var(--border)", borderRadius: 2, marginTop: 6, overflow: "hidden" };
      const progFillStyle = { height: "100%", width: claimed + "%", background: "linear-gradient(90deg, " + SEA + ", var(--gold), " + NER + ")", borderRadius: 2, transition: "width .5s ease" };
      
      const infoStyle = { display: "flex", justifyContent: "space-between", fontSize: 10, color: "var(--faint)", marginTop: 3 };

      const showScore = status === "LIVE" || status === "FINAL";

      return h('div', { className: "header-bar", style: headerStyle },
        h('div', { style: rowStyle },
          // SEA
          h('div', { style: teamLeftStyle },
            h('img', { src: "https://a.espncdn.com/i/teamlogos/nfl/500/sea.png", style: logoStyle, alt: "SEA" }),
            h('div', null,
              h('div', { className: "bebas", style: teamLabelStyle(SEA) }, "SEA"),
              showScore && h('div', { className: "bebas", style: scoreStyle }, totalSea)
            )
          ),
          // Center Status
          h('div', { style: centerStyle },
            status === "FINAL" && h('span', { className: "status-badge final" }, "FINAL"),
            status === "LIVE" && h('span', { className: "status-badge live" }, "LIVE"),
            status === "SOON" && h('span', { className: "status-badge soon" }, "SOON"),
            status === "PRE" && cd && h('div', { style: { display: "flex", gap: 3, justifyContent: "center" } },
              [[cd.h, ":"], [cd.m, ":"], [cd.s, ""]].map(([v, sep], i) => 
                h(React.Fragment, { key: i },
                  h('span', { className: "bebas", style: { fontSize: 14, color: "var(--text)" } }, String(v).padStart(2, "0")),
                  sep && h('span', { style: { color: "var(--faint)", fontSize: 12 } }, sep)
                )
              ),
              cd.d > 0 && h('div', { style: { fontSize: 8, color: "var(--faint)", letterSpacing: 1 } }, cd.d + "D LEFT")
            )
          ),
          // NE
          h('div', { style: teamRightStyle },
            h('div', { style: { textAlign: "right" } },
              h('div', { className: "bebas", style: teamLabelStyle(NER) }, "NE"),
              showScore && h('div', { className: "bebas", style: scoreStyle }, totalNe)
            ),
            h('img', { src: "https://a.espncdn.com/i/teamlogos/nfl/500/ne.png", style: logoStyle, alt: "NE" })
          )
        ),
        // Progress
        h('div', { style: progBarStyle },
          h('div', { style: progFillStyle })
        ),
        // Info
        h('div', { style: infoStyle },
          h('span', null, claimed + "/100"),
          pot > 0 && h('span', { style: { color: "var(--gold)" } }, "💰 $" + pot),
          h('span', null, Object.keys(safeGrid(data.grid).filter(Boolean).reduce((a, n) => ({ ...a, [n]: 1 }), {}) || {}).length + " players")
        )
      );
    }
"""

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Rewrite GameHeader
# Find start
start_match = re.search(r'function GameHeader\s*\(\{', content)
if start_match:
    start_idx = start_match.start()
    # Find end: next function BoardTab
    end_match = re.search(r'function BoardTab', content)
    if end_match:
        end_idx = end_match.start()
        # Find the comment before BoardTab if any
        comment_match = content.rfind("//", start_idx, end_idx)
        if comment_match != -1 and comment_match > start_idx + 100:
             end_idx = comment_match
        
        # Replace
        print(f"Replacing GameHeader from {start_idx} to {end_idx}")
        content = content[:start_idx] + new_game_header + "\n\n" + content[end_idx:]
    else:
        print("BoardTab not found, cannot safely replace GameHeader")

# 2. Global fixes for malformed tags
print("Applying global tag fixes...")
content = content.replace("< div", "<div")
content = content.replace("</div >", "</div>")
content = content.replace("< !--", "<!--")
content = content.replace("-- >", "-->")
content = content.replace("style = ${", "style=${")

# 3. Fix p.o -> p.opts locally just in case
if "p.o.map" in content:
     content = content.replace("p.o.map", "p.opts.map")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Finished fix_corruptions.")
