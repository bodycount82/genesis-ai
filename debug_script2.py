import re

with open('attention-mechanism.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
script = match.group(1)

# Find all ( and ) with line numbers
lines = script.split('\n')
paren_balance = 0
for i, line in enumerate(lines):
    opens = line.count('(')
    closes = line.count(')')
    paren_balance += opens - closes
    if opens != closes:
        print(f'Line {i+1}: balance={paren_balance} ({opens} ( vs {closes} )): {line.strip()[:80]}')

print(f'\nFinal balance: {paren_balance}')
print(f'Total lines: {len(lines)}')

# Show lines where balance goes negative or suspicious
print('\n--- Lines with high closing parens ---')
for i, line in enumerate(lines):
    closes = line.count(')')
    if closes >= 3:
        print(f'Line {i+1} (bal={paren_balance}): {line.strip()[:100]}')
