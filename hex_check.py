
import os

path = r"c:\Users\mathe\OneDrive\Desktop\Fam Super Bowl Squares 2026\index.html"

with open(path, "rb") as f:
    content = f.read()

# Find "SetupScreen"
start_idx = content.find(b"function SetupScreen")
if start_idx != -1:
    # Look for "return html" after that
    ret_idx = content.find(b"return html", start_idx)
    if ret_idx != -1:
        # Grab the next 100 bytes
        chunk = content[ret_idx:ret_idx+100]
        print(f"Hex dump of return block:\n{chunk.hex(' ')}")
        print(f"ASCII interpretation:\n{chunk.decode('utf-8', errors='replace')}")
    else:
        print("return html not found in SetupScreen")
else:
    print("SetupScreen not found")
