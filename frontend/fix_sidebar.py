import glob
import re

files = glob.glob('*.html') + ['generate_pages.py']
for file in files:
    if file == 'index.html':
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Revert to base HTML elements, no collapsed pre-class to avoid conflicts
    content = content.replace('<div class="sidebar collapsed" id="sidebar">', '<div class="sidebar" id="sidebar">')
    
    # We want sidebar to be collapsed natively:
    # 1. replace `transform: translateX(-250px);` temporarily to safely extract rules without overlapping
    content = re.sub(r'\.sidebar\.collapsed\s*\{\s*transform:\s*translateX\(-250px\);\s*\}', '.sidebar.active { transform: translateX(0); }', content)
    
    # Update base sidebar rule to have transform and -250px
    content = re.sub(
        r'(\.sidebar\s*\{[^}]*z-index:\s*1000;\s*)\}',
        r'\1    transform: translateX(-250px);\n        }',
        content
    )
    
    # Update main content rule margin logic
    content = re.sub(
        r'(\.main-content\s*\{[^}]*margin-left:)\s*250px([^}]*\})',
        r'\1 0\2',
        content
    )
    # the expanded class
    content = re.sub(
        r'\.main-content\.expanded\s*\{\s*margin-left:\s*0;\s*\}',
        '.main-content.expanded { margin-left: 250px; }',
        content
    )
    
    # In generate_pages.py, there's double curly braces {{ }}, so we need another sweep for python format safe strings:
    content = re.sub(r'\.sidebar\.collapsed\s*\{\{\s*transform:\s*translateX\(-250px\);\s*\}\}', '.sidebar.active {{ transform: translateX(0); }}', content)
    
    content = re.sub(
        r'(\.main-content\.expanded\s*\{\{\s*margin-left:)\s*0;(\s*\}\})',
        r'\1 250px;\2',
        content
    )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Update Complete")
