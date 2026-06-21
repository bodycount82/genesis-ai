import os, re
hf = [f for f in os.listdir('.') if f.endswith('.html')]
out = []
out.append(f'Files: {len(hf)}')
missing = set()
for f in hf:
    c = open(f, encoding='utf-8').read()
    for m in re.findall(r'href="([^"]*\.html)"', c):
        b = os.path.basename(m)
        if b not in hf:
            missing.add(b)
out.append(f'Unique missing: {len(missing)}')
for m in sorted(missing):
    out.append(m)

# Also check for broken scripts, duplicate styles etc.
broken = []
dup_styles = []
for f in hf:
    c = open(f, encoding='utf-8').read()
    sc = c.count('<style>')
    if sc > 1:
        dup_styles.append(f)
    issues = []
    if '<html' not in c: issues.append('no html')
    if '</html>' not in c: issues.append('no /html')
    if '<head>' not in c: issues.append('no head')
    if '<body>' not in c: issues.append('no body')
    if '<title>' not in c: issues.append('no title')
    if issues:
        broken.append((f, issues))

out.append(f'\nBroken structure: {len(broken)}')
for f, i in broken[:10]:
    out.append(f'  {f}: {i}')
out.append(f'\nDuplicate style tags: {len(dup_styles)}')
for f in dup_styles[:10]:
    out.append(f'  {f}')

# Check all_pages.txt
with open('all_pages.txt', encoding='utf-8') as fh:
    listed = set(l.strip() for l in fh if l.strip())
extra = listed - set(hf)
missing_from_list = set(hf) - listed
out.append(f'\nall_pages.txt extra: {len(extra)}')
for e in sorted(extra)[:10]:
    out.append(f'  {e}')
out.append(f'all_pages.txt missing from list: {len(missing_from_list)}')
for e in sorted(missing_from_list)[:10]:
    out.append(f'  {e}')

# Check queue-behavior.html
with open('index.html', encoding='utf-8') as fh:
    if 'queue-behavior.html' in fh.read():
        out.append('\n*** queue-behavior.html referenced in index.html but MISSING ***')

open('analysis_output.txt', 'w', encoding='utf-8').write('\n'.join(out))
