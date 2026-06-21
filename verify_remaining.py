import re

files = [
    'absence.html',
    'blindsight.html',
    'doubt.html',
    'emergence.html',
    'philosophy-of-mind.html',
    'trust.html'
]

def strip_strings(code):
    code = re.sub(r'`[^`\\]*(?:\\.[^`\\]*)*`', '""', code)
    code = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', code)
    code = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "''", code)
    code = re.sub(r'//[^\n]*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

print("=== RAW COUNT (no stripping) ===")
for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for i, script in enumerate(scripts):
        opens = script.count('(')
        closes = script.count(')')
        status = "BALANCED" if opens == closes else f"UNBALANCED ({opens} vs {closes})"
        print(f"  {fname}: {status}")

print()
print("=== AFTER STRIPPING STRINGS ===")
for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for i, script in enumerate(scripts):
        cleaned = strip_strings(script)
        opens = cleaned.count('(')
        closes = cleaned.count(')')
        status = "BALANCED" if opens == closes else f"UNBALANCED ({opens} vs {closes})"
        print(f"  {fname}: {status}")

print()
print("=== DETAILED: absence.html ===")
with open('absence.html', 'r', encoding='utf-8') as f:
    content = f.read()
match = re.search(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
if match:
    script = match.group(1)
    print(f"Raw: ({script.count('(')} vs {script.count(')')})")
    cleaned = strip_strings(script)
    print(f"Cleaned: ({cleaned.count('(')} vs {cleaned.count(')')})")
    
    # Show what strip_strings changed
    raw_lines = script.split('\n')
    clean_lines = cleaned.split('\n')
    for i, (r, c) in enumerate(zip(raw_lines, clean_lines)):
        if r != c:
            print(f"  Line {i+1} changed:")
            print(f"    RAW:   |{r.strip()[:80]}|")
            print(f"    CLEAN: |{c.strip()[:80]}|")
