import re, os

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

for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the script block between <script> and </script>
    match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if not match:
        print(f"SKIP: {fname} (no script block)")
        continue
    
    script_start = match.start()
    script_end = match.end()
    script_content = match.group(1)
    
    opens = script_content.count('(')
    closes = script_content.count(')')
    diff = closes - opens  # positive means too many )
    
    if diff <= 0:
        print(f"OK: {fname} ({opens} ( vs {closes} ))")
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
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # Verify
    with open(fname, 'r', encoding='utf-8') as f:
        verify = f.read()
    v_match = re.search(r'<script>(.*?)</script>', verify, re.DOTALL)
    if v_match:
        v_opens = v_match.group(1).count('(')
        v_closes = v_match.group(1).count(')')
        print(f"  VERIFIED: {v_opens} ( vs {v_closes})")
