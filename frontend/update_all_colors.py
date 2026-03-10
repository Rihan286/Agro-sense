import os
import glob
import re

html_files = glob.glob('*.html')
templates = ['generate_pages.py']

color_replacements = {
    # Primary Green: #00A30E
    # Dark Green: #1B4716
    # Light Green: #7AD656
    # Sky Blue Accent: #00AAFF
    # Soft Background: #ADFFC7

    # Sidebar background
    '#2e7d32': '#1B4716',
    '#1b5e20': '#00A30E',
    
    # Text colors
    '#2d3319': '#1B4716',
    
    # Body background / soft background
    '#f4f7f6': '#ADFFC7',
    
    # Welcome banner gradient
    'background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)': 'background: linear-gradient(135deg, #ADFFC7 0%, #7AD656 100%)',
    'border-left: 5px solid #2e7d32': 'border-left: 5px solid #00A30E',
    
    # Card styles
    'box-shadow: 0 12px 24px rgba(46, 125, 50, 0.15)': 'box-shadow: 0 12px 24px rgba(0, 163, 14, 0.15)',
    'border-color: #a5d6a7': 'border-color: #7AD656',
    'background: #e8f5e9': 'background: #ADFFC7',
}

for file in html_files + templates:
    if file == 'index.html' or not os.path.exists(file): continue

    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Modify toggle logic
    # In generate_pages.py and dashboard.html, history.html:
    # Sidebar default: left: -250px; or transform: translateX(-250px); -> stays same. 
    # But wait, original code:
    # .sidebar.collapsed { transform: translateX(-250px); }
    # So if we make it collapsed by default, we just add `collapsed` class or invert logic.
    # User wanted "sidebar is collapsed by default".
    # We can just change the HTML: <div class="sidebar collapsed" id="sidebar">
    # Wait, in main content: <div class="main-content" id="main-content"> (no expanded class).
    
    # 1. Colors replacement
    for old_c, new_c in color_replacements.items():
        content = content.replace(old_c, new_c)

    # 2. Add 'collapsed' to sidebar
    content = content.replace('<div class="sidebar" id="sidebar">', '<div class="sidebar collapsed" id="sidebar">')

    # Ensure main content does not have expanded padding initially if we are using toggle('collapsed') and toggle('expanded')
    # If initially collapsed, the JS toggles `collapsed` off? 
    # Let's inspect CSS for .main-content.expanded.

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Theme colors and sidebar defaults injected successfully.")
