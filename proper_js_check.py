import re, os

def strip_js_strings(code):
    """Properly strip all JS strings and comments, preserving code structure."""
    result = []
    i = 0
    n = len(code)
    
    while i < n:
        # Single-line comment
        if code[i:i+2] == '//':
            while i < n and code[i] != '\n':
                i += 1
            continue
        
        # Multi-line comment
        if code[i:i+2] == '/*':
            i += 2
            while i < n - 1 and code[i:i+2] != '*/':
                i += 1
            i += 2  # skip */
            result.append(' ')
            continue
        
        # Template literal
        if code[i] == '`':
            i += 1
            while i < n:
                if code[i] == '\\':
                    i += 2  # skip escaped char
                elif code[i] == '`':
                    i += 1
                    break
                else:
                    i += 1
            result.append('"')
            continue
        
        # Double-quoted string
        if code[i] == '"':
            i += 1
            while i < n and code[i] != '"':
                if code[i] == '\\':
                    i += 1
                i += 1
            i += 1  # skip closing "
            result.append('"')
            continue
        
        # Single-quoted string
        if code[i] == "'":
            i += 1
            while i < n and code[i] != "'":
                if code[i] == '\\':
                    i += 1
                i += 1
            i += 1  # skip closing '
            result.append("'")
            continue
        
        result.append(code[i])
        i += 1
    
    return ''.join(result)

html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])

critical = 0
major = 0
minor = 0
info = 0

for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # CRITICAL checks
    if not content.strip().startswith('<!DOCTYPE'):
        critical += 1
        print(f"CRITICAL: {fname} missing DOCTYPE")
    
    if '</html>' not in content:
        critical += 1
        print(f"CRITICAL: {fname} missing </html>")
    
    # Check JS with proper string stripping
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for i, script in enumerate(scripts):
        cleaned = strip_js_strings(script)
        if cleaned.count('(') != cleaned.count(')'):
            critical += 1
            print(f"CRITICAL: {fname} unbalanced JS (block {i})")
    
    # MAJOR checks
    root_blocks = re.findall(r':root\s*\{', content)
    if len(root_blocks) > 1:
        major += 1
        print(f"MAJOR: {fname} duplicate :root ({len(root_blocks)})")
    
    if 'viewport' not in content:
        major += 1
        print(f"MAJOR: {fname} missing viewport")
    
    if 'box-sizing' not in content:
        major += 1
        print(f"MAJOR: {fname} missing box-sizing")
    
    # MINOR: CSS > 300 lines
    style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if style_match and len(style_match.group(1).split('\n')) > 300:
        minor += 1
        print(f"MINOR: {fname}: {len(style_match.group(1).split(chr(10)))} CSS lines")
    
    # INFO: file size
    if os.path.getsize(fname) > 50000:
        info += 1

print(f"\n{'='*60}")
print(f"RESULTS:")
print(f"  Critical: {critical}")
print(f"  Major: {major}")
print(f"  Minor: {minor}")
print(f"  Info: {info}")
print(f"  Total issues: {critical + major + minor}")
if critical == 0 and major == 0:
    print(f"\nSITE IS READY FOR PUBLISHING!")
