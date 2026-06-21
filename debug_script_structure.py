import re

fname = 'attention-mechanism.html'
with open(fname, 'r', encoding='utf-8') as f:
    content = f.read()

# Find ALL script tags with their positions
for m in re.finditer(r'<script[^>]*>', content):
    print(f"Script tag at position {m.start()}: |{m.group()}|")
    
    # Get everything after this tag until </script>
    after_tag = content[m.end():]
    close_idx = after_tag.find('</script>')
    if close_idx > 0:
        script_content = after_tag[:close_idx]
        print(f"  Script length: {len(script_content)} chars")
        print(f"  First 100 chars: |{script_content[:100]}|")
        print(f"  Last 100 chars: |{script_content[-100:]}|")
        
        opens = script_content.count('(')
        closes = script_content.count(')')
        print(f"  Parens: {opens} ( vs {closes}) diff={closes-opens}")
        
        # Find where the imbalance accumulates
        lines = script_content.split('\n')
        balance = 0
        for i, line in enumerate(lines):
            line_opens = line.count('(')
            line_closes = line.count(')')
            balance += line_opens - line_closes
            if abs(balance) > 3:
                print(f"  Line {i+1}: bal={balance} |{line.strip()[:80]}|")
