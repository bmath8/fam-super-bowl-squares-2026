import re

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add GAME_OVER constant after KICKOFF
if 'const GAME_OVER' not in content:
    content = content.replace(
        'const KICKOFF = new Date("2026-02-08T18:30:00-05:00").getTime();',
        'const KICKOFF = new Date("2026-02-08T18:30:00-05:00").getTime();\n    const GAME_OVER = true; // Disable auto-sync, game is over'
    )
    print("Added GAME_OVER constant")

# Disable auto-sync when GAME_OVER (in useEffect)  
pattern = r'(useEffect\(\(\) => \{\s+)if \(!joined\) return;'
replacement = r'\1if (!joined || GAME_OVER) return; // Skip auto-sync if game over'
content = re.sub(pattern, replacement, content)
print("Modified auto-sync useEffect")

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ GAME_OVER lockdown applied successfully")
