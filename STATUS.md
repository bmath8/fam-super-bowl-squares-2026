# STATUS.md — audited 2026-09-23

**What it is:** Real-time Super Bowl squares app that ran a live family event — 100-square grid, randomized draw, score-driven winner resolution, chat, host controls, and an application-level write lock for post-event read-only safety.

**Stack:** React + Firebase Realtime Database, deployed to both Vercel and Netlify.

**Canonical copy:** `C:\Users\mathe\Dev\fam-super-bowl-squares-2026` — HEAD bf54bdac (2026-07-23, "Merge branch demo-unblock"), 117 commits, working tree effectively clean (1 stray dirty file), remote `bmath8/fam-super-bowl-squares-2026`. This is the copy whose commit timestamp matches GitHub's last-pushed time (2026-09-23T19:45 UTC on the repo page), confirming it is what's actually live.

**Duplicates:**
- `C:\Brian HQ\02_Projects\Other_Projects\Fam Super Bowl Squares 2026` — same commit lineage (112 commits, root matches), but 5 commits behind the Dev copy and stops at 2026-02-08. Stale mirror, safe to archive once confirmed.
- `C:\Brian\02_Projects\fam-super-bowl-squares-2026` — **a completely different git history** (separate root commit, only 2 commits: "SECURITY: Add application-level write lock" + "Add DEMO_MODE, remove hardcoded Firebase config, add README", dated 2026-07-22, one day *before* the canonical Dev copy's final commit). This looks like a manually squashed/sanitized snapshot (possibly for a staging/showcase purpose), not the real project history. It should not be treated as canonical.

**Live check (run today):** https://fam-super-bowl-squares-2026.vercel.app -> 200.

**Deploy:** Vercel project `fam-super-bowl-squares-2026` (prj_bv2QODkuFM4VXfOmAwKPUpPYAAnG), production deployment READY, matches the canonical repo's commit lineage. A Netlify deployment also exists per repo config but was not independently checked today (no Netlify CLI/API call made in this session — mark as unverified).

**Tests:** No automated test run performed today (no test tooling identified in the time available) — do not claim a pass count.

**Security:** DEMO_MODE and hardcoded-Firebase-config removal already landed per commit history (2026-07-22/23), consistent with the "still usable" claim in the GitHub description. Not independently re-scanned for secrets in this pass beyond that commit history check — recommend a full `git grep` secret sweep before any visibility change.

**Recommendation:** SHOWCASE (real-time DB + concurrency/write-lock security story), but low priority to polish further since the GitHub repo already reads well ("Still up and usable"). Top priority is resolving the 3-copy sprawl: keep Dev as canonical, archive/delete the Brian HQ mirror, and clarify whether `Brian\02_Projects` copy is an intentional sanitized snapshot or an accidental fork (ask Brian).
