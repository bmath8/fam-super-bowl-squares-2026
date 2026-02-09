
import re
import os

try:
    with open(r"c:\Users\mathe\OneDrive\Desktop\Fam Super Bowl Squares 2026\index.html", "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r'(trace\("Script-Initialize"\);[\s\S]*?)<\/script>', content)
    if not match:
        match = re.search(r'(const html = htm\.bind[\s\S]*?)<\/script>', content)

    if match:
        js_content = match.group(1)
        with open("debug.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        print("Extracted JS to debug.js")
    else:
        print("Could not find main script block")

except Exception as e:
    print(f"Error: {e}")
