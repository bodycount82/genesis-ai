import os, re

os.chdir(r"D:\Genesis 1.17 crash fix\backend\workspace\web page for publishing")
html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
fixed = 0

for f in html_files:
    c = open(f, encoding='utf-8').read()
    
    # Count style opening and closing tags
    open_count = c.count('<style>')
    close_count = c.count('</style>')
    
    if open_count == 1 and close_count > 1:
        # Single opening but multiple closing - remove extra closings
        new_c = re.sub(r'</style>\s*</style>', '</style>', c)
        if new_c != c:
            open(f, 'w', encoding='utf-8').write(new_c)
            fixed += 1
            print(f"Fixed extra </style> in {f} ({close_count} -> {new_c.count('</style>')})")
    elif open_count > close_count:
        # More opening than closing - find and remove the extra opening
        # This shouldn't happen after our previous fixes, but just in case
        pass

print(f"\nTotal fixed: {fixed}")
