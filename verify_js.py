import re

def strip_strings_and_comments(code):
    code = re.sub(r'`[^`\\]*(?:\\.[^`\\]*)*`', '""', code)
    code = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', code)
    code = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "''", code)
    code = re.sub(r'//[^\n]*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

files = [
    'attention-mechanism.html',
    'cognitive-load.html', 
    'creativity-engine.html',
    'hallucination-explorer.html',
    'inner-world.html',
    'intuition-engine.html',
    'resilience-engine.html',
    'theory-of-mind.html'
]

all_ok = True
for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    if not match:
        print(f"SKIP: {fname}")
        continue
    
    script = match.group(1)
    cleaned = strip_strings_and_comments(script)
    
    opens = cleaned.count('(')
    closes = cleaned.count(')')
    
    if opens == closes:
        print(f"OK: {fname} ({opens} balanced)")
    else:
        all_ok = False
        print(f"BROKEN: {fname} ({opens} ( vs {closes} ))")

print(f"\nAll JS balanced: {all_ok}")
