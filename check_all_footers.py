#!/usr/bin/env python3
"""
Scan all HTML files for footer issues and fix them automatically.
Checks for:
1. Double footers (multiple <footer class="site-footer">)
2. Missing display: contents on .footer-links inside site-footer
3. Bad grid-template-columns (2fr 1fr 1fr instead of proper layout)
4. Old-style <footer class="footer"> mixed with site-footer
"""

import re
from pathlib import Path

BASE = Path(__file__).parent

def check_and_fix(filepath):
    """Check a file for footer issues and fix them."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        issues_found = []
        
        # Check 1: Double site-footers
        sf_matches = list(re.finditer(r'<footer class="site-footer">', content))
        if len(sf_matches) > 1:
            issues_found.append(f'DOUBLE FOOTER ({len(sf_matches)} found)')
            # Remove all but the last one
            for i in range(len(sf_matches) - 1):
                start = sf_matches[i].start()
                # Find matching </footer>
                end = content.find('</footer>', start + 10)
                if end != -1:
                    end += len('</footer>')
                    content = content[:start] + content[end:]
        
        # Check 2: Mixed footer types (old <footer class="footer"> + site-footer)
        if '<footer class="footer">' in content and '<footer class="site-footer">' in content:
            issues_found.append('MIXED FOOTER TYPES')
            pattern = re.compile(r'\s*<!--\s*Footer\s*-->\s*<footer class="footer">.*?</footer>', re.DOTALL)
            match = pattern.search(content)
            if match:
                content = content[:match.start()] + content[match.end():]
        
        # Check 3: site-footer with repeat(3) but missing display: contents on .footer-links
        if '.site-footer' in content and 'repeat(3,' in content:
            if '.site-footer .footer-links { display:' not in content:
                issues_found.append('MISSING display:contents')
                footer_content_match = re.search(r'(\.site-footer\s*\.footer-content\s*\{[^}]+\})', content)
                if footer_content_match:
                    insert_text = '\n.site-footer .footer-links { display: contents; }'
                    content = content[:footer_content_match.end()] + insert_text + content[footer_content_match.end():]
        
        # Check 4: Non-site-footers with bad grid columns
        if '.site-footer' not in content and 'grid-template-columns:' in content:
            gc_match = re.search(r'(grid-template-columns:\s*)2fr\s+1fr\s+1fr', content)
            if gc_match:
                issues_found.append('BAD GRID COLUMNS')
                content = content.replace('2fr 1fr 1fr', 'minmax(200px, 240px) 1fr')
        
        # Write back if changed
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, issues_found
        
        return False, []
    
    except Exception as e:
        print(f"  ERROR: {filepath.name}: {e}")
        return False, [f'ERROR: {str(e)}']


def main():
    html_files = sorted([f for f in BASE.iterdir() if f.suffix == '.html' and f.name != 'index.html'])
    
    fixed_count = 0
    total = len(html_files)
    bad_files = []
    
    print(f"Scanning {total} HTML files...\n")
    
    for i, filepath in enumerate(html_files, 1):
        changed, issues = check_and_fix(filepath)
        
        if issues:
            status = f"[FIXED] {'; '.join(issues)}"
            fixed_count += 1
            bad_files.append((filepath.name, issues))
        else:
            status = "[OK]"
        
        name = filepath.name.encode('utf-8', 'replace').decode()
        print(f"[{i}/{total}] {status} - {name}")
    
    print(f"\n{'='*60}")
    print(f"Fixed: {fixed_count}/{total} files")
    
    if bad_files:
        print(f"\nFiles that had issues (now fixed):")
        for name, issues in bad_files:
            print(f"  - {name}: {'; '.join(issues)}")


if __name__ == '__main__':
    main()
