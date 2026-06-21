#!/usr/bin/env python3
"""
COMPREHENSIVE FOOTER FIX — All HTML files at once.
Fixes:
1. Remove duplicate old <footer class="footer"> when site-footer exists
2. Add display: contents to .site-footer .footer-links (spreads nav sections horizontally)
3. Fix grid-template-columns from "2fr 1fr 1fr" to proper layout for non-site-footers
4. Ensure consistent padding/margins on footer-content
"""

import re
from pathlib import Path

BASE = Path(__file__).parent

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # ============================================================
        # FIX 1: Remove duplicate old-style <footer class="footer"> 
        # when there's also a <footer class="site-footer">
        # This removes the FIRST footer block (old style) and keeps only site-footer
        # ============================================================
        if '<footer class="footer">' in content and '<footer class="site-footer">' in content:
            pattern = re.compile(
                r'\s*<!--\s*Footer\s*-->\s*'
                r'<footer class="footer">.*?</footer>',
                re.DOTALL
            )
            match = pattern.search(content)
            if match:
                content = content[:match.start()] + content[match.end():]
        
        # ============================================================
        # FIX 2: Add display: contents to .site-footer .footer-links
        # so footer-section children become direct grid items under footer-content
        # This fixes the "vertical stacking" issue where nav sections stack in one column
        # ============================================================
        if '.site-footer' in content and 'repeat(3,' in content:
            # Only add if not already present
            if '.site-footer .footer-links { display:' not in content:
                footer_content_match = re.search(
                    r'(\.site-footer\s*\.footer-content\s*\{[^}]+\})', 
                    content
                )
                if footer_content_match:
                    insert_text = '\n.site-footer .footer-links { display: contents; }'
                    content = (content[:footer_content_match.end()] + 
                              insert_text + 
                              content[footer_content_match.end():])
        
        # ============================================================
        # FIX 3: Fix regular footer-content grid columns for non-site-footers
        # Change "2fr 1fr 1fr" to "minmax(200px, 240px) 1fr" 
        # This fixes pages that have brand + links-wrapper as only 2 children
        # ============================================================
        if '.site-footer' not in content:
            old_grid = re.search(r'(grid-template-columns:\s*)2fr\s+1fr\s+1fr', content)
            if old_grid:
                content = content.replace('2fr 1fr 1fr', 'minmax(200px, 240px) 1fr')
        
        # ============================================================
        # FIX 4: Add padding to footer-content for proper margins (non-site-footers only)
        # ============================================================
        if '.site-footer' not in content and '.footer-content' in content:
            fc_block = re.search(r'(\.footer-content\s*\{[^}]+\})', content)
            if fc_block:
                block_text = fc_block.group(1)
                if 'padding:' not in block_text:
                    # Add padding before the closing brace
                    new_block = block_text.rstrip('}') + '; padding: 0 32px; }'
                    content = content.replace(block_text, new_block, 1)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ERROR processing {filepath.name}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    html_files = sorted([f for f in BASE.iterdir() if f.suffix == '.html' and f.name != 'index.html'])
    
    fixed_count = 0
    total = len(html_files)
    
    print(f"Processing {total} HTML files...\n")
    
    for i, filepath in enumerate(html_files, 1):
        changed = fix_file(filepath)
        status = "[FIX]" if changed else "[OK] "
        name = filepath.name.encode('utf-8', 'replace').decode()
        print(f"[{i}/{total}] {status} - {name}")
    
    print(f"\n{'='*60}")
    print(f"Fixed: {fixed_count}/{total} files")


if __name__ == '__main__':
    main()
