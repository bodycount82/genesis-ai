import re, os

files = [
    'absence.html',
    'attention-garden.html',
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

for fname in files:
    fpath = os.path.join('.', fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the script block
    match = re.search(r'(<script[^>]*>)(.*?)(</script>)', content, re.DOTALL)
    if not match:
        print(f"SKIP: {fname} (no script)")
        continue
    
    script_start = match.start()
    script_end = match.end()
    script_content = match.group(2)
    
    # Count parens after stripping strings
    cleaned = strip_strings(script_content)
    opens = cleaned.count('(')
    closes = cleaned.count(')')
    diff = closes - opens  # positive means too many )
    
    if diff <= 0:
        print(f"OK: {fname}")
        continue
    
    print(f"FIXING: {fname} - removing {diff} extra closing parens from end of script")
    
    # Remove excess closing parens from the very end of the script content
    new_script = script_content.rstrip()
    removed = 0
    while removed < diff and new_script.endswith(')'):
        new_script = new_script[:-1]
        removed += 1
    
    if removed < diff:
        print(f"  WARNING: Only removed {removed} of {diff} extra parens")
    
    # Reconstruct the file
    new_content = content[:script_start+9] + new_script + content[script_end-9:]
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # Verify
    with open(fpath, 'r', encoding='utf-8') as f:
        verify = f.read()
    v_match = re.search(r'<script[^>]*>(.*?)</script>', verify, re.DOTALL)
    if v_match:
        v_cleaned = strip_strings(v_match.group(1))
        v_opens = v_cleaned.count('(')
        v_closes = v_cleaned.count(')')
        print(f"  VERIFIED: {v_opens} ( vs {v_closes})")
