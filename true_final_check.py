import re, os

html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
print(f"Total HTML files: {len(html_files)}")
print()

results = {'critical': [], 'major': [], 'minor': [], 'info': []}

for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # CRITICAL: missing DOCTYPE
    if not content.strip().startswith('<!DOCTYPE'):
        results['critical'].append(f"{fname}: missing DOCTYPE")
    
    # CRITICAL: missing </html>
    if '</html>' not in content:
        results['critical'].append(f"{fname}: missing </html>")
    
    # CRITICAL: missing <title>
    if not re.search(r'<title>[^<]+</title>', content):
        results['critical'].append(f"{fname}: missing title")
    
    # CRITICAL: unbalanced JS (raw count - strings don't affect balance)
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for i, script in enumerate(scripts):
        if script.count('(') != script.count(')'):
            results['critical'].append(f"{fname}: unbalanced JS (block {i})")
    
    # CRITICAL: missing </script>
    if len(re.findall(r'<script\b[^>]*>', content)) != len(re.findall(r'</script>', content)):
        results['critical'].append(f"{fname}: missing </script>")
    
    # MAJOR: duplicate :root blocks
    root_blocks = re.findall(r':root\s*\{', content)
    if len(root_blocks) > 1:
        results['major'].append(f"{fname}: {len(root_blocks)} :root blocks")
    
    # MAJOR: missing viewport meta
    if 'viewport' not in content:
        results['major'].append(f"{fname}: missing viewport meta")
    
    # MAJOR: missing box-sizing reset
    if 'box-sizing' not in content:
        results['major'].append(f"{fname}: missing box-sizing")
    
    # MINOR: CSS > 300 lines
    style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if style_match and len(style_match.group(1).split('\n')) > 300:
        results['minor'].append(f"{fname}: {len(style_match.group(1).split(chr(10)))} CSS lines")
    
    # INFO: file size > 50KB
    size = os.path.getsize(fname)
    if size > 50000:
        results['info'].append(f"{fname}: {size} bytes ({size/1024:.1f} KB)")

print("=" * 60)
print("TRUE FINAL VERIFICATION RESULTS")
print("=" * 60)
print()
print(f"CRITICAL issues: {len(results['critical'])}")
for issue in results['critical']:
    print(f"  [CRITICAL] {issue}")

print()
print(f"MAJOR issues: {len(results['major'])}")
for issue in results['major']:
    print(f"  [MAJOR] {issue}")

print()
print(f"MINOR issues: {len(results['minor'])}")
for issue in results['minor']:
    print(f"  [MINOR] {issue}")

print()
print(f"INFO items: {len(results['info'])}")
for issue in results['info']:
    print(f"  [INFO] {issue}")

print()
print("=" * 60)
total = len(results['critical']) + len(results['major']) + len(results['minor'])
if total == 0:
    print("ALL CHECKS PASSED - Site is ready for publishing!")
else:
    print(f"Total issues: {total}")
print("=" * 60)
