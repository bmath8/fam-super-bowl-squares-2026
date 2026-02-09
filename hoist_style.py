
import os

path = r"c:\Users\mathe\OneDrive\Desktop\Fam Super Bowl Squares 2026\index.html"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

setup_screen_idx = -1
for i, line in enumerate(lines):
    if "function SetupScreen" in line:
        setup_screen_idx = i
        break

if setup_screen_idx != -1:
    # We need to find where to insert the style const
    # We can insert it right before "return html"
    
    # First, locate "return html"
    ret_idx = -1
    for j in range(setup_screen_idx, min(setup_screen_idx + 100, len(lines))):
        if "return html" in lines[j]:
            ret_idx = j
            break
    
    if ret_idx != -1:
        # Check if we already refactored?
        if "const containerStyle" in lines[ret_idx-1]:
            print("Already refactored?")
        else:
            # Construct the new style definition
            # We need to extract the NAV variable usage.
            # The original style was:
            # background: "radial-gradient(ellipse at 30% 20%, " + NAV + " 0%, #0a0f18 60%, #10060a 100%)",
            
            style_def = """      const containerStyle = {
        minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
        background: "radial-gradient(ellipse at 30% 20%, " + NAV + " 0%, #0a0f18 60%, #10060a 100%)",
        padding: "24px", position: "relative", overflow: "hidden"
      };\n\n"""
            
            # Insert style definition before return
            lines.insert(ret_idx, style_def)
            
            # Now update the return line.
            # It was something like: return html `<div style=${
            # We want: return html`<div style=${containerStyle}>
            
            # Important: We need to consume the OLD lines that defined the style object.
            # The old style object spanned multiple lines.
            # We need to identify where the old <div> tag ENDS or where the style ENDS.
            # The style looked like: style=${ ... } }>
            
            # Let's verify the current state of lines[ret_idx+1] (because we inserted one, so +1)
            curr_ret_idx = ret_idx + 1
            print(f"Current return line: {repr(lines[curr_ret_idx])}")
            
            # We will aggressively replace the whole return block start.
            # We know the next lines contained the object.
            # We can just COMMENT OUT the old lines or replace them?
            # Replacing is cleaner.
            
            lines[curr_ret_idx] = '      return html`<div style=${containerStyle}>\n'
            
            # Now we need to delete the lines that contained the old style keys.
            # They started with { and ended with }
            # But in the latest version (v4/v5 merged), it was:
            # return html `<div style=${ { ... 
            
            # Let's inspect the next few lines to decide what to delete.
            # We'll just look for the closing }>
            
            scan_idx = curr_ret_idx + 1
            while scan_idx < len(lines):
                line_content = lines[scan_idx].strip()
                if line_content.startswith("minHeight") or line_content.startswith("background") or line_content.startswith("padding") or line_content == "{":
                    lines[scan_idx] = "" # Delete line
                    scan_idx += 1
                elif line_content.startswith("}") and "}>" in lines[scan_idx]:
                    # This is the closing line: } }> or similar
                    lines[scan_idx] = "" 
                    scan_idx += 1
                    break
                elif line_content.startswith("}"):
                    # just closing brace of object
                    lines[scan_idx] = ""
                    scan_idx += 1
                elif line_content.startswith("}>"):
                     lines[scan_idx] = ""
                     scan_idx += 1
                     break
                else:
                    # If we hit <div style or something else, we went too far?
                    if "<div" in line_content:
                        break
                    scan_idx += 1

            print("Refactoring complete.")

lines = [l for l in lines if l != ""]

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)
    
print("Finished hoisting.")
