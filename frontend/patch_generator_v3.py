import os

# Read current generate_pages.py
with open('generate_pages.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract the pages dict string
pages_str_start = text.find('pages = {')
pages_str = text[pages_str_start:]

# The new template string
template = '''template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgroSense - {title}</title>
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/feather-icons"></script>
    <link rel="stylesheet" href="css/styles.css">
    <style>
        :root {{
            --granite: #3F4B3B;
            --hunter-green: #44633F;
            --sea-green: #5A9367;
            --mint-leaf: #5CAB7D;
            --bg-color: #F4F7F5;
            --text-primary: #3F4B3B;
            --text-secondary: rgba(63,75,59,0.7);
        }}

        body {{ 
            font-family: 'Inter', sans-serif; 
            background: linear-gradient(135deg, #F0F4F1 0%, #E5ECE7 100%);
            margin: 0; 
            display: flex; 
            overflow-x: hidden; 
            color: var(--text-primary); 
            min-height: 100vh;
        }}

        /* Reset container to avoid styles.css conflicts */
        .page-container {{ width: 100%; display: flex; }}
        
        /* Sidebar Styles */
        .sidebar {{ 
            width: 260px; 
            background: var(--hunter-green); 
            color: white; 
            height: 100vh; 
            position: fixed; 
            top: 0; 
            left: 0; 
            padding: 24px 0; 
            transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
            z-index: 1000;
            box-shadow: 4px 0 20px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
        }}

        .sidebar-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0 24px;
            margin-bottom: 40px;
        }}
        
        .sidebar-logo {{
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, var(--mint-leaf), var(--sea-green));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 10px rgba(90, 147, 103, 0.4);
            color: white;
        }}

        .sidebar h2 {{ 
            margin: 0; 
            letter-spacing: 0.5px; 
            color: white; 
            font-size: 22px; 
            font-weight: 700;
        }}
        
        .sidebar ul {{ list-style: none; padding: 0 16px; margin: 0; flex-grow: 1; }}
        
        .sidebar ul li {{ 
            margin-bottom: 8px;
            border-radius: 12px;
            cursor: pointer; 
            transition: all 0.3s ease; 
        }}
        
        .sidebar ul li a {{ 
            color: rgba(255,255,255,0.7); 
            text-decoration: none; 
            display: flex; 
            align-items: center;
            padding: 12px 20px; 
            font-size: 15px; 
            font-weight: 500;
            gap: 14px;
            transition: all 0.3s ease;
        }}
        
        .sidebar ul li:hover {{
            background: rgba(255,255,255,0.05);
        }}
        
        .sidebar ul li:hover a {{
            color: white;
            transform: translateX(4px);
        }}
        
        .sidebar ul li.active {{ 
            background: var(--sea-green); 
            box-shadow: 0 4px 15px rgba(90, 147, 103, 0.4);
        }}
        
        .sidebar ul li.active a {{
            color: white;
            font-weight: 600;
        }}

        .sidebar ul li.active:hover a {{
            transform: none;
        }}
        
        .logout-container {{
            padding: 0 16px;
            margin-top: auto;
        }}

        /* Main Content */
        .main-content {{ 
            margin-left: 260px; 
            padding: 40px 50px; 
            flex-grow: 1;
            transition: margin-left 0.4s ease;
            width: calc(100% - 260px);
            box-sizing: border-box;
        }}

        /* Header Styles */
        .header {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 40px; 
        }}
        
        .header-left {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        
        .hamburger {{
            font-size: 24px;
            cursor: pointer;
            color: var(--granite);
            background: none;
            border: none;
            padding: 8px;
            display: none;
            border-radius: 8px;
            transition: background 0.2s;
        }}
        
        .hamburger:hover {{
            background: rgba(63,75,59,0.1);
        }}
        
        .header h1 {{ 
            color: var(--granite); 
            margin: 0; 
            font-size: 28px; 
            font-weight: 700; 
        }}

        /* User Menu */
        .header-actions {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .icon-btn {{
            background: rgba(255,255,255,0.5);
            border: 1px solid rgba(255,255,255,0.6);
            backdrop-filter: blur(10px);
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .icon-btn:hover {{
            color: var(--sea-green);
            background: white;
            box-shadow: 0 4px 12px rgba(90, 147, 103, 0.15);
        }}
        
        .badge {{
            position: absolute;
            top: 10px;
            right: 12px;
            background: #E63946;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            border: 2px solid white;
        }}

        .user-menu {{ 
            display: flex;
            align-items: center;
            gap: 12px;
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.7);
            padding: 6px 16px 6px 6px;
            border-radius: 30px;
            box-shadow: 0 4px 12px rgba(63, 75, 59, 0.05);
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .user-menu:hover {{
            background: rgba(255, 255, 255, 0.8);
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(63, 75, 59, 0.08);
        }}

        .avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--mint-leaf), var(--sea-green));
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 16px;
            box-shadow: 0 2px 8px rgba(90, 147, 103, 0.3);
        }}
        
        .user-info-text {{
            display: flex;
            flex-direction: column;
            line-height: 1.2;
        }}

        .user-name {{ 
            font-weight: 600; 
            color: var(--granite); 
            font-size: 14px;
        }}
        
        .user-role {{
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 2px;
        }}

        .feature-wrapper {{
            max-width: 900px;
            margin: 0 auto;
        }}

        /* Specific modifications for generated card components inside old generated code */
        .card {{
            background: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            border-radius: 20px !important;
            box-shadow: 0 8px 24px rgba(63, 75, 59, 0.04) !important;
            transition: all 0.3s ease !important;
        }}

        .card-header h2 {{
            color: var(--granite) !important;
            font-family: 'Inter', sans-serif !important;
        }}

        .card-icon {{
            background: rgba(90, 147, 103, 0.1) !important;
            color: var(--sea-green) !important;
        }}

        .btn-primary {{
            background: var(--sea-green) !important;
            border-radius: 12px !important;
        }}
        .btn-primary:hover {{
            background: var(--mint-leaf) !important;
        }}
        .btn-secondary {{
            background: var(--hunter-green) !important;
            border-radius: 12px !important;
        }}
        .btn-secondary:hover {{
            background: var(--sea-green) !important;
        }}

        @media (max-width: 1024px) {{
            .main-content {{
                padding: 30px;
            }}
        }}

        @media (max-width: 768px) {{
            .sidebar {{ transform: translateX(-100%); }}
            .sidebar.active {{ transform: translateX(0); }}
            .main-content {{ margin-left: 0; width: 100%; padding: 24px 20px; }}
            .header {{ align-items: center; }}
            .user-info-text {{ display: none; }}
            .icon-btn {{ display: none; }}
            .hamburger {{ display: block; }}
        }}
    </style>
</head>
<body>

    <div class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <div class="sidebar-logo">
                <i data-feather="leaf" fill="currentColor" stroke="none" width="20" height="20"></i>
            </div>
            <h2>AgroSense</h2>
        </div>
        
        <ul>
            <li>
                <a href="dashboard.html">
                    <i data-feather="grid" width="20" height="20"></i> Dashboard
                </a>
            </li>
            <li class="{active_detect}">
                <a href="detect.html">
                    <i data-feather="camera" width="20" height="20"></i> Detect Disease
                </a>
            </li>
            <li class="{active_weather}">
                <a href="weather.html">
                    <i data-feather="cloud-rain" width="20" height="20"></i> Weather
                </a>
            </li>
            <li class="{active_market}">
                <a href="market.html">
                    <i data-feather="trending-up" width="20" height="20"></i> Market Prices
                </a>
            </li>
            <li class="{active_assistant}">
                <a href="assistant.html">
                    <i data-feather="message-square" width="20" height="20"></i> AI Assistant
                </a>
            </li>
            <li class="{active_history}">
                <a href="history.html">
                    <i data-feather="clock" width="20" height="20"></i> Detection History
                </a>
            </li>
        </ul>

        <div class="logout-container">
            <ul>
                <li>
                    <a href="#" id="logout-btn">
                        <i data-feather="log-out" width="20" height="20"></i> Logout
                    </a>
                </li>
            </ul>
        </div>
    </div>

    <div class="main-content" id="main-content">
        <div class="header">
            <div class="header-left">
                <button class="hamburger" id="hamburger-btn">
                    <i data-feather="menu"></i>
                </button>
                <h1>{title}</h1>
            </div>
            
            <div class="header-actions">
                <button class="icon-btn">
                    <i data-feather="bell" width="20" height="20"></i>
                    <span class="badge"></span>
                </button>
                
                <div class="user-menu">
                    <div class="avatar" id="avatar-initial">F</div>
                    <div class="user-info-text">
                        <span class="user-name" id="farmer-name">Loading...</span>
                        <span class="user-role">Premium Farmer</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="feature-wrapper">
            {content}
        </div>
    </div>

    <script src="js/main.js"></script>
    <script>
        feather.replace();
        setTimeout(() => {{
            const nameEl = document.getElementById('farmer-name');
            if(nameEl && nameEl.innerText && nameEl.innerText !== 'Loading...') {{
                document.getElementById('avatar-initial').innerText = nameEl.innerText.charAt(0).toUpperCase();
            }}
        }}, 500);
    </script>
</body>
</html>
"""\n\n'''

with open('generate_pages.py', 'w', encoding='utf-8') as f:
    f.write('import os\n\n' + template + pages_str)

print("generate_pages.py has been completely rewritten with the new dashboard frame.")
