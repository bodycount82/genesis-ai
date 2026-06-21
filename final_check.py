import re, os

html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
print(f"Total HTML files: {len(html_files)}")
print()

results = {
    'critical': [],
    'major': [],
    'minor': [],
    'info': []
}

# 1. Check for actual JS errors (after stripping strings)
def strip_strings(code):
    code = re.sub(r'`[^`\\]*(?:\\.[^`\\]*)*`', '""', code)
    code = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', code)
    code = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "''", code)
    code = re.sub(r'//[^\n]*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Critical: missing </script>
    script_opens = len(re.findall(r'<script\b[^>]*>', content))
    script_closes = len(re.findall(r'</script>', content))
    if script_opens != script_closes:
        results['critical'].append(f"{fname}: missing </script>")
    
    # Critical: unbalanced JS parens (after stripping strings)
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for i, script in enumerate(scripts):
        cleaned = strip_strings(script)
        if cleaned.count('(') != cleaned.count(')'):
            results['critical'].append(f"{fname}: unbalanced JS (block {i})")
    
    # Critical: missing DOCTYPE
    if not content.strip().startswith('<!DOCTYPE'):
        results['critical'].append(f"{fname}: missing DOCTYPE")
    
    # Critical: missing </html>
    if '</html>' not in content:
        results['critical'].append(f"{fname}: missing </html>")
    
    # Critical: missing <title>
    if not re.search(r'<title>[^<]+</title>', content):
        results['critical'].append(f"{fname}: missing title")
    
    # Major: duplicate :root blocks
    root_blocks = re.findall(r':root\s*\{', content)
    if len(root_blocks) > 1:
        results['major'].append(f"{fname}: {len(root_blocks)} :root blocks")
    
    # Major: missing viewport meta
    if 'viewport' not in content:
        results['major'].append(f"{fname}: missing viewport meta")
    
    # Major: missing box-sizing reset
    if 'box-sizing' not in content:
        results['major'].append(f"{fname}: missing box-sizing")
    
    # Minor: CSS > 300 lines
    style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if style_match and len(style_match.group(1).split('\n')) > 300:
        results['minor'].append(f"{fname}: {len(style_match.group(1).split(chr(10)))} CSS lines")
    
    # Minor: file size > 50KB
    size = os.path.getsize(fname)
    if size > 50000:
        results['info'].append(f"{fname}: {size} bytes ({size/1024:.1f} KB)")

print("=" * 60)
print("FINAL VERIFICATION RESULTS")
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
    print(f"Total issues: {total} (Critical: {len(results['critical'])}, Major: {len(results['major'])}, Minor: {len(results['minor'])})")
print("=" * 60)
