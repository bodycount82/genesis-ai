import re

def strip_strings_and_comments(code):
    """Remove all string literals and comments from JS code, keeping only code."""
    # Remove template literals (backtick strings)
    code = re.sub(r'`[^`\\]*(?:\\.[^`\\]*)*`', '""', code)
    # Remove double-quoted strings
    code = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', code)
    # Remove single-quoted strings
    code = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "''", code)
    # Remove single-line comments
    code = re.sub(r'//[^\n]*', '', code)
    # Remove multi-line comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

with open('attention-mechanism.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
script = match.group(1)

# Strip strings and comments
cleaned = strip_strings_and_comments(script)

opens = cleaned.count('(')
closes = cleaned.count(')')
print(f'After stripping strings/comments: {opens} ( vs {closes}) diff={closes-opens}')

if opens != closes:
    # Find where the imbalance is
    lines = script.split('\n')
    clean_lines = cleaned.split('\n')
    balance = 0
    for i, (line, clean_line) in enumerate(zip(lines, clean_lines)):
        line_opens = clean_line.count('(')
        line_closes = clean_line.count(')')
        balance += line_opens - line_closes
        if abs(balance) > 2:
            print(f'Line {i+1}: balance={balance} ({line_opens} ( vs {line_closes} )): {line.strip()[:80]}')

    print(f'\nFinal balance: {balance}')
else:
    print('BALANCED! The original count was wrong due to string parens.')
