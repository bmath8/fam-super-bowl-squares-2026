
import os
import re

path = r"c:\Users\mathe\OneDrive\Desktop\Fam Super Bowl Squares 2026\index.html"

# Pure JS BoardTab
new_board_tab = """    // ── Board Tab (Pure JS) ──────────────────────────────────────
    function BoardTab({ data, myName, dbr, toast }) {
      const h = React.createElement;
      const [showMine, setShowMine] = useState(false);
      const [zoom, setZoom] = useState(false);
      const allNames = useMemo(() => [...new Set(safeGrid(data.grid).filter(Boolean) || [])], [data.grid]);
      const myCt = useMemo(() => {
        if (!Array.isArray(data.grid)) return 0;
        return safeGrid(data.grid).filter(n => n === myName).length;
      }, [data.grid, myName]);

      const isConfirmed = data.playerMeta?.[myName]?.confirmed;
      const claimed = useMemo(() => {
        if (!Array.isArray(data.grid)) return 0;
        return safeGrid(data.grid).filter(Boolean).length;
      }, [data.grid]);

      const maxPP = data.settings?.maxPerPlayer || 0;
      const justClaimedRef = useRef(null);

      // Find current quarter winners
      const qWinners = useMemo(() => {
        if (!data.colNums || !data.rowNums) return {};
        const w = {};
        QS.forEach((q, i) => {
          const ss = (data.scores?.SEA || [])[i], ns = (data.scores?.NE || [])[i];
          if (ss != null && ns != null) {
            const cumS = data.scores.SEA.slice(0, i + 1).reduce((a, b) => a + (b || 0), 0);
            const cumN = data.scores.NE.slice(0, i + 1).reduce((a, b) => a + (b || 0), 0);
            const winner = getWinner(data.grid, data.colNums, data.rowNums, cumS, cumN);
            if (winner) {
              const ci = data.colNums.indexOf(cumS % 10), ri = data.rowNums.indexOf(cumN % 10);
              w[ri + "-" + ci] = { quarter: q, winner };
            }
          }
        });
        return w;
      }, [data]);

      const claimSquare = (r, c) => {
        if (!data.grid || !data.grid[r]) return;
        const currentCell = data.grid[r][c];
        if (!myName || myName.trim() === "") { toast("❌ No name set!"); return; }
        if (!dbr) { toast("⏳ Connecting..."); return; }
        if (isConfirmed) { toast("🔒 Picks locked!"); return; }
        if (data.isLocked) { toast("🔒 Board locked!"); return; }
        if (currentCell) { toast("Taken by " + currentCell); return; }
        if (maxPP > 0 && myCt >= maxPP) { toast("Max " + maxPP + " reached"); return; }

        toast("⏳ Claiming...");
        dbr.child("grid").child(String(r)).child(String(c)).set(myName)
           .then(() => { playSound("claim"); toast("✅ Claimed!"); if (navigator.vibrate) navigator.vibrate(50); })
           .catch(err => toast("❌ Failed: " + err.message));
      };

      const unclaimSquare = (r, c) => {
         if (!dbr) return;
         if (isConfirmed || data.isLocked) return toast("🔒 Locked!");
         const current = (data.grid && data.grid[r]) ? data.grid[r][c] : null;
         if (current !== myName) return toast("❌ Not yours!");
         dbr.child("grid").child(String(r)).child(String(c)).remove()
            .then(() => { playSound("claim"); toast("🗑 Removed"); })
            .catch(err => toast("❌ Failed: " + err.message));
      };
      
      const lockBoard = () => {
         if (!dbr) return;
         toast("🔒 Locking...");
         dbr.child("isLocked").set(true).then(() => {
            toast("✅ Locked!");
            const newColNums = Array.from({ length: 10 }, (_, i) => i).sort(() => Math.random() - 0.5);
            const newRowNums = Array.from({ length: 10 }, (_, i) => i).sort(() => Math.random() - 0.5);
            dbr.update({ colNums: newColNums, rowNums: newRowNums });
         });
      };
      
      const quickPick = (n) => {
         if(!dbr || isConfirmed || data.isLocked) return toast("Cannot quick pick");
         const avail = [];
         data.grid.forEach((row, r) => row.forEach((cell, c) => { if (!cell) avail.push([r, c]); }));
         if (avail.length === 0) return toast("Full!");
         const pick = Math.min(n, maxPP > 0 ? maxPP - myCt : n, avail.length);
         if (pick <= 0) return toast("Max reached");
         const shuffled = avail.sort(() => Math.random() - 0.5).slice(0, pick);
         const promises = shuffled.map(([r, c]) => dbr.child("grid").child(String(r)).child(String(c)).set(myName));
         Promise.all(promises).then(() => { playSound("claim"); toast("Got " + pick); });
      };

      // Styles
      const mainStyle = { padding: "4px 4px", animation: "fadeIn .3s ease", flex: 1, display: "flex", flexDirection: "column", justifyContent: "center" };
      const btnBase = { padding: "6px 14px", borderRadius: 8, fontSize: 12, fontWeight: 600, border: "1px solid var(--border2)", background: "transparent", color: "var(--soft)" };

      return h('div', { style: mainStyle },
        // Admin Lock
        !data.isLocked && h('div', { style: { background: "#EF4444", padding: 16, textAlign: "center", marginBottom: 10, borderRadius: 8 } },
           h('div', { style: { color: "#fff", fontWeight: 800, marginBottom: 8 } }, "⚠️ ADMIN: UNLOCKED"),
           h('button', { onClick: lockBoard, style: { background: "#fff", color: "#EF4444", border: "none", padding: "8px 16px", borderRadius: 6, fontWeight: 900 } }, "LOCK & ROLL")
        ),
        
        // Controls
        h('div', { style: { display: "flex", gap: 6, marginBottom: 10, justifyContent: "center" } },
           h('button', { onClick: () => setShowMine(!showMine), style: { ...btnBase, background: showMine ? "var(--gold-glow)" : "transparent", borderColor: showMine ? "var(--gold)" : "var(--border2)", color: showMine ? "var(--gold)" : "var(--soft)" } }, showMine ? "👁 All" : "⭐ Mine"),
           h('button', { onClick: () => setZoom(!zoom), style: { ...btnBase, background: zoom ? "rgba(59,130,246,0.1)" : "transparent", borderColor: zoom ? "var(--accent)" : "var(--border2)", color: zoom ? "var(--accent)" : "var(--soft)" } }, zoom ? "🔍 Out" : "🔍 Zoom"),
           !data.isLocked && [1,5].map(n => h('button', { key: n, onClick: () => quickPick(n), style: { ...btnBase, background: "var(--card)", color: "var(--text)" } }, "🎲 " + n))
        ),

        // Grid
        h('div', { style: { display: "flex", alignItems: "center" } },
           h('div', { style: { writingMode: "vertical-lr", transform: "rotate(180deg)", width: 14, textAlign: "center", color: NER, fontSize: 12, letterSpacing: 2 } }, "NE"),
           h('div', { style: { flex: 1, overflowX: zoom ? "auto" : "hidden" } },
              h('div', { className: "sq-grid", style: { minWidth: zoom ? 600 : "100%" } },
                 h('div', { className: "sq-hdr", style: { background: "transparent" } }),
                 Array.from({ length: 10 }).map((_, c) => h('div', { key: "h"+c, className: "sq-hdr", style: { color: data.colNums ? SEA : "var(--faint)", background: data.colNums ? SEA+"22" : "var(--card)" } }, data.colNums ? data.colNums[c] : "?")),
                 (Array.isArray(data.grid) ? data.grid : []).map((row, r) => h(React.Fragment, { key: r },
                    h('div', { className: "sq-hdr", style: { color: data.rowNums ? NER : "var(--faint)", background: data.rowNums ? NER+"22" : "var(--card)" } }, data.rowNums ? data.rowNums[r] : "?"),
                    row.map((cell, c) => {
                       const mine = cell === myName;
                       const isWin = qWinners[r+"-"+c];
                       const color = cell ? getPlayerColor(cell, allNames) : null;
                       const hidden = showMine && cell && !mine;
                       return h('div', {
                          key: c,
                          className: "sq-cell " + (cell ? "claimed" : "empty") + (mine ? " mine" : "") + (isWin ? " winner" : "") + (hidden ? " dimmed" : ""),
                          style: { background: cell ? color : undefined, borderColor: cell ? "#fff" : undefined },
                          onClick: () => !cell ? claimSquare(r, c) : (cell === myName ? unclaimSquare(r, c) : toast("Taken by " + cell))
                       },
                         cell && h('span', { style: { fontSize: "clamp(12px,3vw,18px)", pointerEvents: "none" } }, getPlayerEmoji(data.playerMeta, cell)),
                         cell && h('span', { style: { fontSize: "clamp(8px,2vw,10px)", fontWeight: 900, color: "#fff" } }, cell.substring(0,4).toUpperCase()),
                         isWin && h('span', { style: { position: "absolute", top: 2, right: 2, fontSize: 8, background: "var(--gold)", color: "#000", padding: "1px 3px", borderRadius: 4 } }, isWin.quarter)
                       );
                    })
                 ))
              )
           )
        ),
        
        // Legend
         h('div', { style: { display: "flex", flexWrap: "wrap", gap: 6, marginTop: 10, justifyContent: "center" } },
            allNames.map(name => h('div', { key: name, style: { fontSize: 11, padding: "2px 6px", borderRadius: 4, background: getPlayerColor(name, allNames)+"22", color: getPlayerColor(name, allNames), border: "1px solid "+getPlayerColor(name, allNames)+"44" } }, 
               getPlayerEmoji(data.playerMeta, name), " ", name, " (" + safeGrid(data.grid).filter(n => n === name).length + ")"
            ))
         )
      );
    }
"""

new_scores_tab = """    // ── Scores Tab (Pure JS) ─────────────────────────────────────
    function ScoresTab({ data, dbr, toast }) {
      const h = React.createElement;
      const [editing, setEditing] = useState(null);
      const [tempSea, setTempSea] = useState("");
      const [tempNe, setTempNe] = useState("");
      const claimed = safeGrid(data.grid).filter(Boolean).length || 0;
      const pps = data.pool?.pricePerSquare || 0;
      const totalPot = claimed * pps;
      const split = data.pool?.payoutSplit || [25, 25, 25, 25];

      const saveScore = (qi) => {
         const s = parseInt(tempSea), n = parseInt(tempNe);
         if (isNaN(s) || isNaN(n)) return toast("Invalid");
         const newSea = [...(data.scores?.SEA || [null,null,null,null])];
         const newNe = [...(data.scores?.NE || [null,null,null,null])];
         newSea[qi] = s; newNe[qi] = n;
         dbr.update({ scores: { SEA: newSea, NE: newNe } });
         setEditing(null);
      };

      return h('div', { style: { padding: 16, animation: "fadeIn .3s ease" } },
         QS.map((q, i) => {
            const seaQ = (data.scores?.SEA || [])[i], neQ = (data.scores?.NE || [])[i];
            const hasSc = seaQ != null && neQ != null;
            const cumS = data.scores?.SEA?.slice(0, i+1).reduce((a,b)=>a+(b||0),0)||0;
            const cumN = data.scores?.NE?.slice(0, i+1).reduce((a,b)=>a+(b||0),0)||0;
            const winner = hasSc && data.colNums ? getWinner(data.grid, data.colNums, data.rowNums, cumS, cumN) : null;
            const payout = Math.round(totalPot * split[i] / 100);

            return h('div', { key: q, style: { background: "var(--card)", borderRadius: 12, padding: 14, border: "1px solid " + (winner ? "var(--gold)" : "var(--border)"), marginBottom: 12 } },
               h('div', { style: { display: "flex", justifyContent: "space-between", alignItems: "center" } },
                  h('div', { style: { display: "flex", gap: 8 } }, 
                     h('span', { className: "bebas", style: { color: "var(--gold)" } }, q),
                     payout > 0 && h('span', { style: { fontSize: 11, background: "var(--gold-glow)", color: "var(--gold)", padding: "2px 8px", borderRadius: 99 } }, "$" + payout)
                  ),
                  hasSc ? h('div', { className: "bebas" }, "SEA " + cumS + " - NE " + cumN) :
                  (editing?.q === i ? h('div', { style: { display: "flex", gap: 4 } },
                     h('input', { value: tempSea, onChange: e => setTempSea(e.target.value), placeholder: "SEA", style: { width: 30, background: "var(--input)", color: "#fff", border: "none" } }),
                     h('input', { value: tempNe, onChange: e => setTempNe(e.target.value), placeholder: "NE", style: { width: 30, background: "var(--input)", color: "#fff", border: "none" } }),
                     h('button', { onClick: () => saveScore(i), style: { background: "var(--gold)", border: "none", padding: "2px 6px", borderRadius: 4 } }, "Save")
                  ) : h('button', { onClick: () => setEditing({ q: i }), style: { background: "transparent", border: "1px solid var(--border)", color: "var(--soft)", fontSize: 10 } }, "Edit"))
               ),
               winner && h('div', { style: { marginTop: 8, padding: 8, background: "linear-gradient(45deg, var(--gold) 0%, #B8892E 100%)", borderRadius: 8, color: "#000", fontWeight: 800, textAlign: "center" } }, 
                  "WINNER: " + winner
               )
            );
         })
      );
    }
"""

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace range from BoardTab start to ChatTab start
start_match = re.search(r'function BoardTab', content)
if start_match:
    start_idx = start_match.start()
    
    # End is ChatTab
    # Also we need to make sure we include the broken "PropsTab" stuff in the range to DELETE it.
    # ChatTab usually follows the broken block.
    
    end_match = re.search(r'function ChatTab', content)
    
    if end_match:
        end_idx = end_match.start()
        
        # Check if there is a "Global Error Handler" block before ChatTab
        err_match = re.search(r'// ── Global Error Handler', content)
        if err_match and err_match.start() > start_idx and err_match.start() < end_idx:
             # We want to keep Error Handler? No, the Error Handler was inside the garbage block?
             # Wait, look at view_file.
             # Line 1458: // ── Global Error Handler
             # This was AFTER the garbage PropsTab code.
             # So we should probably keep it if it's cleaner.
             # But if it is DUPLICATE, we should delete it.
             pass
        
        # Important: The view_file showed:
        # 1253: // ── Scores Tab
        # ...
        # 1458: // ── Global Error Handler
        # 1466: function ChatTab
        
        # So replacing from BoardTab start (953) to ChatTab start (1466) covers:
        # BoardTab (broken)
        # ScoresTab (broken logic, corrupted template)
        # Garbage PropsTab inside ScoresTab
        # Global Error Handler (duplicated?)
        
        # Re-insert Error Handler?
        # Use existing if simpler.
        
        # To be safe, I will replace up to ChatTab. And insert new BoardTab/ScoresTab.
        # I will leave out Global Error Handler (it's likely defined at top of file anyway?
        # Top of file had window.onerror.
        # Line 1460 redefined window.onerror.
        # I'll just skip it.
        
        print(f"Replacing range {start_idx} to {end_idx}")
        content = content[:start_idx] + new_board_tab + "\n\n" + new_scores_tab + "\n\n" + content[end_idx:]
        
    else:
        print("ChatTab not found")
else:
    print("BoardTab not found")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Finished fix_tabs.")
