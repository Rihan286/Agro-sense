import os
import re

html_files = [
    'dashboard.html',
    'detect.html',
    'weather.html',
    'market.html',
    'assistant.html',
    'history.html'
]

# 1. Update main.js
main_js_path = 'js/main.js'
with open(main_js_path, 'r', encoding='utf-8') as f:
    main_content = f.read()

layout_script = """
// ===== Common Layout Logic =====
const userDataStr = localStorage.getItem('agrosense_user');
if (userDataStr) {
    try {
        const userData = JSON.parse(userDataStr);
        const fname = document.getElementById('farmer-name');
        if (fname) fname.textContent = userData.name;
    } catch(e) {}
}

const logoutBtn = document.getElementById('logout-btn');
if (logoutBtn) logoutBtn.addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.removeItem('agrosense_token');
    localStorage.removeItem('agrosense_user');
    window.location.href = 'login.html';
});

const globHamburgerBtn = document.getElementById('hamburger-btn');
const globSidebar = document.getElementById('sidebar');
const globMainContent = document.getElementById('main-content');

if (globHamburgerBtn) globHamburgerBtn.addEventListener('click', () => {
    if (window.innerWidth <= 768) {
        if (globSidebar) globSidebar.classList.toggle('active');
    } else {
        if (globSidebar) globSidebar.classList.toggle('collapsed');
        if (globMainContent) globMainContent.classList.toggle('expanded');
    }
});
"""

if '// ===== Common Layout Logic =====' not in main_content:
    main_content = main_content.replace('// ===== DOM Elements =====', layout_script + '\n// ===== DOM Elements =====')
    with open(main_js_path, 'w', encoding='utf-8') as f:
        f.write(main_content)

# 2. Clean up HTML files
for file in html_files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove old inline scripts that collide with main.js
        content = re.sub(r'// Check Auth.*?window\.location\.href = \'login\.html\';\s+\}', '', content, flags=re.DOTALL)
        content = re.sub(r'// Load Farmer Name.*?document\.getElementById\(\'farmer-name\'\)\.textContent = userData\.name;\s+\}', '', content, flags=re.DOTALL)
        content = re.sub(r'// Logout.*?window\.location\.href = \'login\.html\';\s+\}\);', '', content, flags=re.DOTALL)
        content = re.sub(r'// Sidebar Toggle Logic.*?\}\}\);', '', content, flags=re.DOTALL)
        content = re.sub(r'const token = localStorage\.getItem\(\'agrosense_token\'\);', '', content)
        
        # Ensure we don't have empty script tags hanging
        content = re.sub(r'<script>\s*</script>', '', content)
        
        # add main.js to those that dont have it
        if 'src="js/main.js"' not in content:
            content = content.replace('</body>', '    <script src="js/main.js"></script>\n</body>')
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Fixed scripts across all files!")
