import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

matches = list(re.finditer(r'href=["\']#["\']', content))
print(f'Found {len(matches)} href="#" in index.html')
for m in matches:
    start = max(0, m.start()-30)
    end = min(len(content), m.end()+30)
    print(f'  ...{content[start:end]}...')
