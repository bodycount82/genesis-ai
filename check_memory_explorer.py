import re

with open('memory-system-explorer.html', 'r', encoding='utf-8') as f:
    content = f.read()

results = []

# Check tab switching function exists
if 'function switchTab' in content:
    results.append('switchTab function: FOUND')
else:
    results.append('switchTab function: MISSING')

# Check onclick handlers on tab buttons
tab_buttons = re.findall(r'<button[^>]*onclick=["\']([^"\']+)["\'][^>]*>', content)
results.append(f'Tab button onclick handlers: {len(tab_buttons)}')
for btn in tab_buttons:
    results.append(f'  - {btn}')

# Check tab content divs exist
tab_contents = re.findall(r'id=["\']tab-([^"\']+)["\']', content)
results.append(f'Tab content divs: {tab_contents}')

# Check for JS errors (proper string stripping)
def strip_js_strings(code):
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
    cleaned = strip_js_strings(script)
    opens = cleaned.count('(')
    closes = cleaned.count(')')
    status = 'BALANCED' if opens == closes else f'UNBALANCED ({opens} vs {closes})'
    results.append(f'Script block {i}: {status}')

with open('memory_explorer_check.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))

print('DONE - check memory_explorer_check.txt')
