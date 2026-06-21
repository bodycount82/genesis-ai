import re

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
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for i, script in enumerate(scripts):
        cleaned = strip_strings(script)
        opens = cleaned.count('(')
        closes = cleaned.count(')')
        
        if opens != closes:
            print(f"=== {fname} (block {i}) ===")
            print(f"  {opens} ( vs {closes}) diff={closes-opens}")
            
            # Find lines where imbalance accumulates
            lines = cleaned.split('\n')
            balance = 0
            for j, line in enumerate(lines):
                line_opens = line.count('(')
                line_closes = line.count(')')
                balance += line_opens - line_closes
                if abs(balance) > 2:
                    print(f"  Line {j+1}: bal={balance} ({line_opens} ( vs {line_closes} )): {line.strip()[:80]}")
            
            # Show last 10 lines
            print(f"  Last 10 lines:")
            for line in lines[-10:]:
                print(f"    |{line.strip()}|")
            print()
