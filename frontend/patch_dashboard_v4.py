import os

html_dashboard = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgroSense - Dashboard</title>
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/feather-icons"></script>
    <style>
        :root {
            --granite: #3F4B3B;
            --hunter-green: #44633F;
            --sea-green: #5A9367;
            --mint-leaf: #5CAB7D;
            --bg-color: #F4F7F5;
            --text-primary: #3F4B3B;
            --text-secondary: rgba(63,75,59,0.7);
        }

        body { 
            font-family: 'Inter', sans-serif; 
            background: linear-gradient(135deg, #F0F4F1 0%, #E5ECE7 100%);
            margin: 0; 
            display: flex; 
            overflow-x: hidden; 
            color: var(--text-primary); 
            min-height: 100vh;
        }

        .sidebar { 
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
        }

        .sidebar-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0 24px;
            margin-bottom: 40px;
        }

        .sidebar ul { list-style: none; padding: 0 16px; margin: 0; flex-grow: 1; }
        .sidebar ul li { margin-bottom: 8px; border-radius: 12px; cursor: pointer; transition: all 0.3s ease; }
        .sidebar ul li a { 
            color: rgba(255,255,255,0.7); text-decoration: none; display: flex; align-items: center;
            padding: 12px 20px; font-size: 15px; font-weight: 500; gap: 14px; transition: all 0.3s ease;
        }
        
        .sidebar ul li:hover { background: rgba(255,255,255,0.08); }
        .sidebar ul li:hover a { color: white; transform: translateX(4px); }
        .sidebar ul li.active { background: linear-gradient(90deg, var(--sea-green), var(--mint-leaf)); box-shadow: 0 4px 15px rgba(90, 147, 103, 0.4); }
        .sidebar ul li.active a { color: white; font-weight: 600; }
        .sidebar ul li.active:hover a { transform: none; }
        
        .logout-container { padding: 0 16px; margin-top: auto; }

        .main-content { 
            margin-left: 260px; padding: 40px 50px; flex-grow: 1; transition: margin-left 0.4s ease;
            width: calc(100% - 260px); box-sizing: border-box;
            animation: fadeIn 0.4s ease-out;
        }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }
        .header-left { display: flex; align-items: center; gap: 20px; }
        .hamburger { font-size: 24px; cursor: pointer; color: var(--granite); background: none; border: none; padding: 8px; display: none; border-radius: 8px; }
        .header h1 { color: var(--granite); margin: 0; font-size: 28px; font-weight: 700; }

        .header-actions { display: flex; align-items: center; gap: 16px; }

        .icon-btn {
            background: rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.6); backdrop-filter: blur(10px);
            width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
            color: var(--text-secondary); cursor: pointer; transition: all 0.3s ease; position: relative;
        }
        .icon-btn:hover { color: var(--mint-leaf); background: white; box-shadow: 0 4px 12px rgba(90, 147, 103, 0.15); transform: translateY(-2px); }
        .badge { position: absolute; top: 10px; right: 12px; background: #E63946; width: 8px; height: 8px; border-radius: 50%; border: 2px solid white; }

        .user-menu-wrapper { position: relative; }
        .user-menu { 
            display: flex; align-items: center; gap: 12px; background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.7); padding: 6px 16px 6px 6px; border-radius: 30px;
            box-shadow: 0 4px 12px rgba(63, 75, 59, 0.05); cursor: pointer; transition: all 0.3s ease;
        }
        .user-menu:hover { background: rgba(255, 255, 255, 0.9); transform: translateY(-2px); box-shadow: 0 6px 16px rgba(63, 75, 59, 0.1); }
        .user-menu:active { transform: translateY(0); }

        .avatar {
            width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, var(--mint-leaf), var(--sea-green));
            color: white; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 16px;
            box-shadow: 0 2px 8px rgba(90, 147, 103, 0.3);
        }
        .user-info-text { display: flex; flex-direction: column; line-height: 1.2; }
        .user-name { font-weight: 600; color: var(--granite); font-size: 14px; }
        .user-role { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }

        /* Dropdown Panel */
        .dropdown-panel {
            position: absolute; top: calc(100% + 12px); right: 0; width: 240px; background: rgba(255,255,255,0.95); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
            border-radius: 16px; box-shadow: 0 16px 40px rgba(63, 75, 59, 0.15); border: 1px solid rgba(255,255,255,0.6);
            opacity: 0; visibility: hidden; transform: translateY(-10px); transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1); z-index: 100; padding: 8px 0;
        }
        .dropdown-panel.show { opacity: 1; visibility: visible; transform: translateY(0); }
        .dropdown-profile { display: flex; align-items: center; gap: 12px; padding: 16px 20px; }
        .avatar-large { width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, var(--mint-leaf), var(--sea-green)); color: white; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 18px; }
        .dropdown-user-details { display: flex; flex-direction: column; }
        .d-user-name { font-weight: 600; color: var(--granite); font-size: 15px; }
        .d-user-role { font-size: 12px; color: var(--text-secondary); }
        .dropdown-divider { height: 1px; background: rgba(0,0,0,0.06); margin: 8px 0; }
        .dropdown-item { display: flex; align-items: center; gap: 12px; padding: 12px 20px; color: var(--granite); text-decoration: none; font-size: 14px; font-weight: 500; transition: all 0.2s; }
        .dropdown-item i { width: 18px; height: 18px; color: var(--mint-leaf); transition: color 0.2s; }
        .dropdown-item:hover { background: rgba(92, 171, 125, 0.08); color: var(--mint-leaf); padding-left: 24px; }
        .dropdown-item.text-danger:hover { background: rgba(230, 57, 70, 0.08); color: #E63946; }
        .dropdown-item.text-danger:hover i { color: #E63946; }

        /* Hero Banner */
        .hero-banner {
            position: relative;
            background: url('https://images.unsplash.com/photo-1592982537447-6f2cf32f9157?q=80&w=2000&auto=format&fit=crop') center 60%/cover no-repeat;
            border-radius: 20px; padding: 60px 50px; margin-bottom: 40px; box-shadow: 0 16px 40px rgba(63, 75, 59, 0.15); overflow: hidden; display: flex; flex-direction: column; justify-content: flex-end; min-height: 240px;
        }
        .hero-banner::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(135deg, rgba(68, 99, 63, 0.75) 0%, rgba(90, 147, 103, 0.45) 100%); z-index: 1; backdrop-filter: blur(2px); -webkit-backdrop-filter: blur(2px);
        }
        .hero-profile-inline {
            position: absolute; top: 20px; right: 20px; z-index: 3; background: rgba(255,255,255,0.25);
            backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); padding: 8px 16px; border-radius: 30px;
            display: flex; align-items: center; gap: 10px; border: 1px solid rgba(255,255,255,0.4); color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .hero-profile-inline .star {
            width: 24px; height: 24px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--mint-leaf); font-weight: bold; font-size: 12px;
        }
        .hero-content { position: relative; z-index: 2; color: white; max-width: 650px; }
        .hero-label {
            display: inline-block; background: rgba(255,255,255,0.2); backdrop-filter: blur(8px); padding: 6px 12px; border-radius: 20px;
            font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.3);
        }
        .hero-content h2 { margin: 0 0 16px 0; font-size: 34px; font-weight: 700; text-shadow: 0 2px 10px rgba(0,0,0,0.15); line-height: 1.2; }
        .hero-content p { font-size: 16px; line-height: 1.6; margin: 0; color: rgba(255,255,255,0.95); }

        /* Cards Grid */
        .cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 24px; }
        .card { 
            background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
            padding: 32px 24px; border-radius: 20px; box-shadow: 0 4px 16px rgba(63, 75, 59, 0.04); text-align: center; cursor: pointer;
            transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1); text-decoration: none; display: flex; flex-direction: column; align-items: center; border: 2px solid transparent; position: relative;
        }
        .card:hover { transform: translateY(-8px) scale(1.02); box-shadow: 0 16px 32px rgba(92, 171, 125, 0.15), 0 0 0 2px var(--mint-leaf); }
        .card-icon {
            font-size: 32px; margin-bottom: 24px; background: rgba(90, 147, 103, 0.1); width: 72px; height: 72px; display: flex; align-items: center; justify-content: center;
            border-radius: 50%; color: var(--sea-green); transition: all 0.3s ease;
        }
        .card:hover .card-icon { transform: scale(1.1); background: linear-gradient(135deg, var(--mint-leaf), var(--sea-green)); color: white; box-shadow: 0 8px 20px rgba(92, 171, 125, 0.3); }
        .card h3 { color: var(--granite); margin: 0 0 12px 0; font-size: 18px; font-weight: 600; }
        .card p { color: var(--text-secondary); font-size: 14px; margin: 0; line-height: 1.5; }

        @media (max-width: 1024px) { .main-content { padding: 30px; } }
        @media (max-width: 768px) {
            .sidebar { transform: translateX(-100%); } .sidebar.active { transform: translateX(0); }
            .main-content { margin-left: 0; width: 100%; padding: 24px 20px; }
            .hamburger { display: block; } .hero-banner { padding: 40px 24px; border-radius: 20px; }
            .hero-content h2 { font-size: 26px; } .user-menu { padding: 6px 12px 6px 6px; }
            .user-info-text, .hero-profile-inline, .icon-btn { display: none; } .cards { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

    <div class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <div class="brand-logo" style="display: flex; align-items: center; gap: 12px;">
                <svg width="36" height="36" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="40" height="40" rx="10" fill="url(#paint0_linear)"/>
                    <path d="M20 10C20 10 12 14 12 22C12 28 20 32 20 32C20 32 28 28 28 22C28 14 20 10 20 10Z" fill="white"/>
                    <path d="M20 32V22" stroke="#5A9367" stroke-width="2" stroke-linecap="round"/>
                    <defs>
                        <linearGradient id="paint0_linear" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
                            <stop stop-color="#5CAB7D"/>
                            <stop offset="1" stop-color="#5A9367"/>
                        </linearGradient>
                    </defs>
                </svg>
                <h2 style="margin: 0; color: white; font-size: 22px; font-weight: 700; letter-spacing: 0.5px;">AgroSense</h2>
            </div>
        </div>
        
        <ul>
            <li class="active"><a href="dashboard.html"><i data-feather="grid" width="20" height="20"></i> Dashboard</a></li>
            <li><a href="detect.html"><i data-feather="camera" width="20" height="20"></i> Detect Disease</a></li>
            <li><a href="weather.html"><i data-feather="cloud-rain" width="20" height="20"></i> Weather</a></li>
            <li><a href="market.html"><i data-feather="trending-up" width="20" height="20"></i> Market Prices</a></li>
            <li><a href="assistant.html"><i data-feather="message-square" width="20" height="20"></i> AI Assistant</a></li>
            <li><a href="history.html"><i data-feather="clock" width="20" height="20"></i> Detection History</a></li>
        </ul>
        <div class="logout-container">
            <ul><li><a href="#" id="sidebar-logout-btn"><i data-feather="log-out" width="20" height="20"></i> Logout</a></li></ul>
        </div>
    </div>

    <div class="main-content" id="main-content">
        <div class="header">
            <div class="header-left">
                <button class="hamburger" id="hamburger-btn"><i data-feather="menu"></i></button>
                <h1>Farmer Dashboard</h1>
            </div>
            
            <div class="header-actions">
                <button class="icon-btn">
                    <i data-feather="bell" width="20" height="20"></i>
                    <span class="badge"></span>
                </button>
                
                <div class="user-menu-wrapper">
                    <div class="user-menu" id="user-menu-btn">
                        <div class="avatar" id="avatar-initial">F</div>
                        <div class="user-info-text">
                            <span class="user-name" id="farmer-name">Loading...</span>
                            <span class="user-role">Premium Farmer</span>
                        </div>
                    </div>
                    
                    <div class="dropdown-panel" id="user-dropdown">
                        <div class="dropdown-profile">
                            <div class="avatar-large" id="dropdown-initial">F</div>
                            <div class="dropdown-user-details">
                                <span class="d-user-name" id="dropdown-name">Loading...</span>
                                <span class="d-user-role">Premium Farmer</span>
                            </div>
                        </div>
                        <div class="dropdown-divider"></div>
                        <a href="#" class="dropdown-item"><i data-feather="user"></i> Profile</a>
                        <a href="#" class="dropdown-item"><i data-feather="settings"></i> My Account</a>
                        <a href="#" class="dropdown-item"><i data-feather="sliders"></i> Settings</a>
                        <a href="history.html" class="dropdown-item"><i data-feather="clock"></i> Detection History</a>
                        <a href="#" class="dropdown-item"><i data-feather="help-circle"></i> Help / Support</a>
                        <div class="dropdown-divider"></div>
                        <a href="#" class="dropdown-item text-danger" id="dropdown-logout"><i data-feather="log-out"></i> Logout</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="hero-banner">
            <div class="hero-profile-inline">
                <div class="star">★</div>
                <span style="font-size: 13px; font-weight: 600; letter-spacing: 0.5px;">PRO FARMER</span>
            </div>
            <div class="hero-content">
                <span class="hero-label">Smart Agriculture</span>
                <h2>Welcome to AgroSense</h2>
                <p>Your AI powered smart farming assistant helping detect crop diseases, track weather patterns, and monitor real-time market prices.</p>
            </div>
        </div>

        <div class="cards">
            <a href="detect.html" class="card">
                <div class="card-icon"><i data-feather="camera" width="32" height="32"></i></div>
                <h3>Detect Disease</h3>
                <p>Upload a photo of your crop to instantly identify diseases and get AI treatment advice.</p>
            </a>
            <a href="weather.html" class="card">
                <div class="card-icon"><i data-feather="cloud-drizzle" width="32" height="32"></i></div>
                <h3>Weather Forecast</h3>
                <p>Check highly accurate local weather conditions and farming advisories.</p>
            </a>
            <a href="market.html" class="card">
                <div class="card-icon"><i data-feather="bar-chart-2" width="32" height="32"></i></div>
                <h3>Market Prices</h3>
                <p>Track the latest live mandi prices for your crops to make informed selling decisions.</p>
            </a>
            <a href="assistant.html" class="card">
                <div class="card-icon"><i data-feather="message-circle" width="32" height="32"></i></div>
                <h3>AI Assistant</h3>
                <p>Chat with our Gemini-powered AI expert for answers to any farming-related questions.</p>
            </a>
        </div>
    </div>
    
    <script src="js/main.js"></script>
    <script>
        feather.replace();
        
        // Setup UI details not connected to main.js logic
        setTimeout(() => {
            const nameEl = document.getElementById('farmer-name');
            if(nameEl && nameEl.innerText && nameEl.innerText !== 'Loading...') {
                const initial = nameEl.innerText.charAt(0).toUpperCase();
                document.getElementById('avatar-initial').innerText = initial;
                const ddInitial = document.getElementById('dropdown-initial');
                const ddName = document.getElementById('dropdown-name');
                if (ddInitial) ddInitial.innerText = initial;
                if (ddName) ddName.innerText = nameEl.innerText;
            }
        }, 600);
    </script>
</body>
</html>
"""

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_dashboard)

print("dashboard.html beautifully updated!")
