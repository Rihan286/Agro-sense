import glob
import re
import os

files = glob.glob('*.html')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update index.html
    if file == 'index.html':
        content = content.replace('--primary-green: #00A30E;', '--primary-green: #87A330;')
        content = content.replace('--dark-green: #1B4716;', '--dark-green: #243010;')
        content = content.replace('--light-green: #7AD656;', '--light-green: #A1C349;')
        content = content.replace('--soft-bg: #ADFFC7;', '--soft-bg: #CAD593;')

    # 2. Update login / signup
    if file in ['login.html', 'signup.html']:
        content = content.replace('background-color: #ADFFC7;', 'background-color: #CAD593;')
        content = content.replace('color: #1B4716;', 'color: #243010;')
        content = content.replace('background: #4caf50;', 'background: #87A330;')
        content = content.replace('background: #388e3c;', 'background: #A1C349;')

    # 3. Update the generated sub-pages
    if file not in ['index.html', 'dashboard.html', 'login.html', 'signup.html']:
        # Exact replacement of generated layout block
        old_css = """        body { font-family: 'Poppins', sans-serif; background-color: #ADFFC7; margin: 0; display: flex; overflow-x: hidden; }
        
        /* Reset container to avoid styles.css conflicts */
        .page-container { width: 100%; display: flex; }
        
        .sidebar { 
            width: 250px; 
            background: #1B4716; 
            color: white; 
            height: 100vh; 
            position: fixed; 
            top: 0; 
            left: 0; 
            padding-top: 20px; 
            transition: transform 0.3s ease;
            z-index: 1000;
            transform: translateX(-250px);
        }
        .sidebar.active { transform: translateX(0); }
        .sidebar h2 { text-align: center; margin-bottom: 30px; letter-spacing: 1px; font-family: 'Poppins', sans-serif; font-size: 24px; font-weight: bold; color: white; }
        .sidebar ul { list-style: none; padding: 0; margin: 0; }
        .sidebar ul li { padding: 15px 20px; border-bottom: 1px solid rgba(255,255,255,0.1); cursor: pointer; transition: 0.3s; }
        .sidebar ul li:hover, .sidebar ul li.active { background: #00A30E; }
        .sidebar ul li a { color: white; text-decoration: none; display: block; font-size: 16px; font-family: 'Poppins', sans-serif; }
        
        .main-content { 
            margin-left: 0; 
            padding: 30px; 
            flex-grow: 1;
            transition: margin-left 0.3s ease;
            width: 100%;
            box-sizing: border-box;
            min-height: 100vh;
        }
        .main-content.expanded { margin-left: 250px; }

        .header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 30px; 
            border-bottom: 2px solid #ddd; 
            padding-bottom: 15px; 
        }
        .header-left { display: flex; align-items: center; gap: 15px; }
        .hamburger { font-size: 24px; cursor: pointer; color: #1B4716; background: none; border: none; padding: 5px; transition: color 0.3s; display: flex; align-items: center; justify-content: center; }
        .hamburger:hover { color: #00A30E; }
        .header h1 { color: #333; margin: 0; font-size: 24px; font-family: 'Poppins', sans-serif; }
        .user-info { font-weight: 500; color: #555; font-family: 'Poppins', sans-serif; }"""

        new_css = """        body { font-family: 'Poppins', sans-serif; background-color: #CAD593; margin: 0; display: flex; overflow-x: hidden; color: #243010; }
        
        /* Reset container to avoid styles.css conflicts */
        .page-container { width: 100%; display: flex; }
        
        .sidebar { 
            width: 250px; 
            background: #2A3C24; 
            color: white; 
            height: 100vh; 
            position: fixed; 
            top: 0; 
            left: 0; 
            padding-top: 20px; 
            transition: transform 0.3s ease;
            z-index: 1000;
            transform: translateX(-250px);
        }
        .sidebar.active { transform: translateX(0); }
        .sidebar h2 { text-align: center; margin-bottom: 30px; letter-spacing: 1px; font-family: 'Poppins', sans-serif; font-size: 24px; font-weight: bold; color: #CAD593; }
        .sidebar ul { list-style: none; padding: 0; margin: 0; }
        .sidebar ul li { padding: 15px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); cursor: pointer; transition: 0.3s; }
        .sidebar ul li:hover, .sidebar ul li.active { background: #87A330; }
        .sidebar ul li a { color: white; text-decoration: none; display: block; font-size: 16px; font-weight: 500; font-family: 'Poppins', sans-serif; }
        
        .main-content { 
            margin-left: 0; 
            padding: 30px; 
            flex-grow: 1;
            transition: margin-left 0.3s ease;
            width: 100%;
            box-sizing: border-box;
            min-height: 100vh;
        }
        .main-content.expanded { margin-left: 250px; }

        .header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 30px; 
            border-bottom: 2px solid rgba(36, 48, 16, 0.1); 
            padding-bottom: 15px; 
        }
        .header-left { display: flex; align-items: center; gap: 15px; }
        .hamburger { font-size: 24px; cursor: pointer; color: #243010; background: none; border: none; padding: 5px; transition: color 0.3s; display: flex; align-items: center; justify-content: center; }
        .hamburger:hover { color: #87A330; }
        .header h1 { color: #243010; margin: 0; font-size: 24px; font-family: 'Poppins', sans-serif; font-weight: 600; }
        .user-info { font-weight: 500; color: #2A3C24; font-family: 'Poppins', sans-serif; }"""
        
        if old_css in content:
            content = content.replace(old_css, new_css)
            
        content = content.replace('color: #1B4716;"', 'color: #243010;"')
        content = content.replace('color: white; font-size: 0.95rem; font-weight:600;', 'color: white; font-size: 0.95rem; font-weight:600; text-shadow: 0px 1px 2px rgba(36, 48, 16, 0.3);')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Theme updated successfully on all pages.")
