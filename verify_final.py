import os, re

html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
print('Files:', len(html_files))
issues = {'js': 0, 'script': 0, 'root': 0, 'hash': 0, 'css': 0, 'size': 0}

for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # JS parens
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for s in scripts:
        if s.count('(') != s.count(')'):
            issues['js'] += 1
    
    # Script close
    if len(re.findall(r'<script\b', content)) != len(re.findall(r'</script>', content)):
        issues['script'] += 1
    
    # Duplicate :root
    if len(re.findall(r':root\s*\{', content)) > 1:
        issues['root'] += 1
    
    # href="#"
    if re.search(r'href=["\']#["\']', content):
        issues['hash'] += 1
    
    # CSS too long
    style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if style_match:
        if len(style_match.group(1).split('\n')) > 300:
            issues['css'] += 1
    
    # File size
    if os.path.getsize(fname) > 50000:
        issues['size'] += 1

print('Issues:', issues)
total = sum(issues.values())
print('Total:', total)

# List remaining specific issues
print()
print('Files with JS paren issues:')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for s in scripts:
        if s.count('(') != s.count(')'):
            print(f'  {fname}')

print()
print('Files with duplicate :root:')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if len(re.findall(r':root\s*\{', content)) > 1:
        print(f'  {fname}')

print()
print('Files with href="#":')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if re.search(r'href=["\']#["\']', content):
        print(f'  {fname}')

print()
print('Files with CSS > 300 lines:')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if style_match and len(style_match.group(1).split('\n')) > 300:
        print(f'  {fname}: {len(style_match.group(1).split(chr(10)))} lines')

print()
print('Files > 50KB:')
for fname in html_files:
    size = os.path.getsize(fname)
    if size > 50000:
        print(f'  {fname}: {size} bytes')
