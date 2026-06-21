#!/usr/bin/env python3
"""Fix pages with duplicate <style> tags - removes the SECOND (duplicate) style block."""
import os, re

os.chdir(r"D:\Genesis 1.17 crash fix\backend\workspace\web page for publishing")

html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
fixed_count = 0
skipped = 0

for f in html_files:
    c = open(f, encoding='utf-8').read()
    
    # Count style tags
    sc = c.count('<style>')
    if sc < 2:
        continue
    
    # Find all style blocks with their positions
    style_positions = []
    for m in re.finditer(r'<style>', c):
        style_positions.append(m.start())
    
    if len(style_positions) < 2:
        continue
    
    # Get content of first and second style blocks
    start1 = style_positions[0]
    end1_match = re.search(r'</style>', c[start1:])
    if not end1_match:
        skipped += 1
        continue
    end1 = start1 + end1_match.end()
    
    start2 = style_positions[1]
    end2_match = re.search(r'</style>', c[start2:])
    if not end2_match:
        skipped += 1
        continue
    end2 = start2 + end2_match.end()
    
    block1 = c[start1:end1]  # <style>...content1...</style>
    block2 = c[start2:end2]  # <style>...content2...</style>
    
    # Normalize for comparison (strip whitespace and comments)
    def normalize(s):
        s = re.sub(r'/\*.*?\*/', '', s, flags=re.DOTALL)
        return re.sub(r'\s+', ' ', s).strip()
    
    if normalize(block1) == normalize(block2):
        # Second block is a duplicate - remove it
        # Remove from start of second <style> to end of second </style>
        new_c = c[:start2] + c[end2:]
        open(f, 'w', encoding='utf-8').write(new_c)
        fixed_count += 1
        print(f"Fixed (duplicate): {f}")
    else:
        # Check if they share the same CSS variables/theme
        b1_clean = re.sub(r'/\*.*?\*/', '', block1, flags=re.DOTALL).strip()
        b2_clean = re.sub(r'/\*.*?\*/', '', block2, flags=re.DOTALL).strip()
        
        # If both have the same :root variables, second is likely a duplicate theme injection
        if '--bg:' in b1_clean and '--bg:' in b2_clean:
            new_c = c[:start2] + c[end2:]
            open(f, 'w', encoding='utf-8').write(new_c)
            fixed_count += 1
            print(f"Merged (theme dup): {f}")
        else:
            skipped += 1
            # Print first 50 chars of each for debugging
            print(f"DIFFERENT in {f}: '{b1_clean[:50]}...' vs '{b2_clean[:50]}...'")

print(f"\nTotal fixed: {fixed_count}")
print(f"Skipped (different blocks): {skipped}")
