import re, os

with open('attention-mechanism.html', 'r', encoding='utf-8') as f:
    content = f.read()

results = []

# Find ALL script tags
scripts = list(re.finditer(r'<script[^>]*>(.*?)</script>', content, re.DOTALL))
results.append(f'Found {len(scripts)} script blocks')
for i, s in enumerate(scripts):
    opens = s.group(1).count('(')
    closes = s.group(1).count(')')
    results.append(f'  Block {i}: {opens} ( vs {closes}) diff={closes-opens}')

# Check what's at the end of the last script block
if scripts:
    last = scripts[-1]
    tail = last.group(1)[-200:]
    results.append('Last script block ends with:')
    for line in tail.split('\n')[-5:]:
        results.append(f'  |{line.strip()}|')

# Check the raw content around </script>
idx = content.find('</script>')
if idx > 0:
    context = content[idx-100:idx+20]
    results.append(f'Context around first </script>: |{context}|')

# Check if there are multiple </script> tags
all_script_closes = list(re.finditer(r'</script>', content))
results.append(f'Total </script> tags: {len(all_script_closes)}')

# Check the raw bytes around script tag
idx2 = content.find('<script>')
if idx2 > 0:
    context2 = content[idx2-10:idx2+50]
    results.append(f'Raw around <script>: |{context2}|')

with open('debug_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))

print('DONE - check debug_output.txt')
