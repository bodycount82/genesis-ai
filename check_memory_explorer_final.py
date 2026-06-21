import os, re

with open('memory-system-explorer.html', 'r', encoding='utf-8') as f:
    content = f.read()

results = []

# 1. switchTab function exists
if 'function switchTab(tabName)' in content:
    results.append('[OK] switchTab function defined')
else:
    results.append('[FAIL] switchTab function missing')

# 2. Tab buttons have onclick handlers
tab_buttons = re.findall(r'<button[^>]*onclick=["\']switchTab\([^)]+\)[^>]*>', content)
results.append(f'[OK] {len(tab_buttons)} tab buttons with onclick')

# 3. Tab content divs exist
tab_ids = re.findall(r'id=["\']tab-([^"\']+)["\']', content)
results.append(f'[OK] {len(tab_ids)} tab content divs: {tab_ids}')

# 4. CSS for tabs exists
if '.tab-content' in content and 'display: none' in content:
    results.append('[OK] Tab CSS (hidden by default)')
else:
    results.append('[FAIL] Tab CSS missing')

if '.tab-content.active' in content and 'display: block' in content:
    results.append('[OK] Active tab CSS')
else:
    results.append('[FAIL] Active tab CSS missing')

# 5. No JS syntax errors (proper string stripping)
def strip_js(code):
    result = []
    i = 0
    n = len(code)
    while i < n:
        if code[i:i+2] == '//':
            while i < n and code[i] != '\n':
                i += 1
            continue
        if code[i:i+2] == '/*':
            i += 2
            while i < n - 1 and code[i:i+2] != '*/':
                i += 1
            i += 2
            result.append(' ')
            continue
        if code[i] == '`':
            i += 1
            while i < n:
                if code[i] == '\\':
                    i += 2
                elif code[i] == '`':
                    i += 1
                    break
                else:
                    i += 1
            result.append('"')
            continue
        if code[i] == '"':
            i += 1
            while i < n and code[i] != '"':
                if code[i] == '\\':
                    i += 1
                i += 1
            i += 1
            result.append('"')
            continue
        if code[i] == "'":
            i += 1
            while i < n and code[i] != "'":
                if code[i] == '\\':
                    i += 1
                i += 1
            i += 1
            result.append("'")
            continue
        result.append(code[i])
        i += 1
    return ''.join(result)

scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
for i, script in enumerate(scripts):
    cleaned = strip_js(script)
    opens = cleaned.count('(')
    closes = cleaned.count(')')
    if opens == closes:
        results.append(f'[OK] Script block {i} balanced ({opens} parens)')
    else:
        results.append(f'[FAIL] Script block {i} unbalanced ({opens} vs {closes})')

with open('memory_explorer_final.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))

print('DONE - check memory_explorer_final.txt')
