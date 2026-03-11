import os

file = 'generate_pages.py'

with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the overall CSS block in generate_pages.py
old_css = """    <style>
        /* Sidebar & Layout Styles */
        body {{ font-family: 'Poppins', sans-serif; background-color: #ADFFC7; margin: 0; display: flex; overflow-x: hidden; }}
        
        /* Reset container to avoid styles.css conflicts */
        .page-container {{ width: 100%; display: flex; }}
        
        .sidebar {{ 
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
        }}
        .sidebar.active {{ transform: translateX(0); }}
        .sidebar h2 {{ text-align: center; margin-bottom: 30px; letter-spacing: 1px; font-family: 'Poppins', sans-serif; font-size: 24px; font-weight: bold; color: white; }}
        .sidebar ul {{ list-style: none; padding: 0; margin: 0; }}
        .sidebar ul li {{ padding: 15px 20px; border-bottom: 1px solid rgba(255,255,255,0.1); cursor: pointer; transition: 0.3s; }}
        .sidebar ul li:hover, .sidebar ul li.active {{ background: #00A30E; }}
        .sidebar ul li a {{ color: white; text-decoration: none; display: block; font-size: 16px; font-family: 'Poppins', sans-serif; }}
        
        .main-content {{ 
            margin-left: 0; 
            padding: 30px; 
            flex-grow: 1;
            transition: margin-left 0.3s ease;
            width: 100%;
            box-sizing: border-box;
            min-height: 100vh;
        }}
        .main-content.expanded {{ margin-left: 250px; }}

        .header {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 30px; 
            border-bottom: 2px solid #ddd; 
            padding-bottom: 15px; 
        }}
        .header-left {{ display: flex; align-items: center; gap: 15px; }}
        .hamburger {{ font-size: 24px; cursor: pointer; color: #1B4716; background: none; border: none; padding: 5px; transition: color 0.3s; display: flex; align-items: center; justify-content: center; }}
        .hamburger:hover {{ color: #00A30E; }}
        .header h1 {{ color: #333; margin: 0; font-size: 24px; font-family: 'Poppins', sans-serif; }}
        .user-info {{ font-weight: 500; color: #555; font-family: 'Poppins', sans-serif; }}

        /* Feature specific wrapper */
        .feature-wrapper {{
            max-width: 900px;
            margin: 0 auto;
        }}

        @media (max-width: 768px) {{
            .sidebar {{ transform: translateX(-250px); }}
            .sidebar.active {{ transform: translateX(0); }}
            .main-content {{ margin-left: 0; padding: 20px; }}
            .header {{ flex-direction: column; align-items: flex-start; gap: 15px; }}
            .user-info {{ align-self: flex-end; }}
        }}
    </style>"""

new_css = """    <style>
        /* Sidebar & Layout Styles */
        body {{ font-family: 'Poppins', sans-serif; background-color: #CAD593; margin: 0; display: flex; overflow-x: hidden; color: #243010; }}
        
        /* Reset container to avoid styles.css conflicts */
        .page-container {{ width: 100%; display: flex; }}
        
        .sidebar {{ 
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
        }}
        .sidebar.active {{ transform: translateX(0); }}
        .sidebar h2 {{ text-align: center; margin-bottom: 30px; letter-spacing: 1px; font-family: 'Poppins', sans-serif; font-size: 24px; font-weight: bold; color: #CAD593; }}
        .sidebar ul {{ list-style: none; padding: 0; margin: 0; }}
        .sidebar ul li {{ padding: 15px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); cursor: pointer; transition: 0.3s; }}
        .sidebar ul li:hover, .sidebar ul li.active {{ background: #87A330; }}
        .sidebar ul li a {{ color: white; text-decoration: none; display: block; font-size: 16px; font-weight: 500; font-family: 'Poppins', sans-serif; }}
        
        .main-content {{ 
            margin-left: 0; 
            padding: 30px; 
            flex-grow: 1;
            transition: margin-left 0.3s ease;
            width: 100%;
            box-sizing: border-box;
            min-height: 100vh;
        }}
        .main-content.expanded {{ margin-left: 250px; }}

        .header {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 30px; 
            border-bottom: 2px solid rgba(36, 48, 16, 0.1); 
            padding-bottom: 15px; 
        }}
        .header-left {{ display: flex; align-items: center; gap: 15px; }}
        .hamburger {{ font-size: 24px; cursor: pointer; color: #243010; background: none; border: none; padding: 5px; transition: color 0.3s; display: flex; align-items: center; justify-content: center; }}
        .hamburger:hover {{ color: #87A330; }}
        .header h1 {{ color: #243010; margin: 0; font-size: 24px; font-family: 'Poppins', sans-serif; font-weight: 600; }}
        .user-info {{ font-weight: 500; color: #2A3C24; font-family: 'Poppins', sans-serif; }}

        /* Feature specific wrapper */
        .feature-wrapper {{
            max-width: 900px;
            margin: 0 auto;
        }}

        @media (max-width: 768px) {{
            .sidebar {{ transform: translateX(-250px); }}
            .sidebar.active {{ transform: translateX(0); }}
            .main-content {{ margin-left: 0; padding: 20px; }}
            .header {{ flex-direction: column; align-items: flex-start; gap: 15px; }}
            .user-info {{ align-self: flex-end; }}
            .hamburger {{ display: block; }}
        }}
    </style>"""

if old_css in content:
    content = content.replace(old_css, new_css)
else:
    print("Warning: CSS string mismatch")

content = content.replace('color: #1B4716;"', 'color: #243010;"')
content = content.replace('d:\\\\Agro Sense\\\\Agro-sense-main\\\\frontend\\\\{key}.html', '{key}.html')

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("generate_pages.py is updated!")
