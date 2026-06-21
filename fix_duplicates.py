import os, re

os.chdir(r"D:\Genesis 1.17 crash fix\backend\workspace\web page for publishing")
dup = []
for f in sorted(os.listdir('.')):
    if not f.endswith('.html'): continue
    c = open(f, encoding='utf-8').read()
    sc = c.count('<style>')
    if sc > 1:
        dup.append((f, sc))

with open('dup_style_report.txt', 'w', encoding='utf-8') as out:
    out.write('Pages with duplicate <style> tags:\n')
    for f, sc in dup:
        out.write(f'  {f}: {sc} style tags\n')
    out.write(f'\nTotal: {len(dup)}\n')

# Now fix them
fixed = 0
for f, sc in dup:
    c = open(f, encoding='utf-8').read()
    
    # Find all <style>...</style> blocks
    style_blocks = re.findall(r'<style>(.*?)</style>', c, re.DOTALL)
    
    if len(style_blocks) < 2:
        continue
    
    # Merge all style blocks into one
    merged_css = '\n'.join(style_blocks)
    
    # Remove all existing <style>...</style> and replace with single merged one
    new_content = re.sub(r'<style>.*?</style>', '<style>\n' + merged_css.strip() + '\n</style>', c, count=0, flags=re.DOTALL)
    
    # Write back
    open(f, 'w', encoding='utf-8').write(new_content)
    fixed += 1

with open('dup_style_report.txt', 'a', encoding='utf-8') as out:
    out.write(f'\nFixed {fixed} pages.\n')

print(f'Fixed {fixed} pages with duplicate <style> tags.')
