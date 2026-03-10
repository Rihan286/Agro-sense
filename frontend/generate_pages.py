import os

template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgroSense - {title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Bitter:wght@400;600;700;800&family=Work+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/styles.css">
    <style>
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
    </style>
</head>
<body>

    <div class="sidebar" id="sidebar">
        <h2>AgroSense</h2>
        <ul>
            <li><a href="dashboard.html">Dashboard</a></li>
            <li class="{active_detect}"><a href="detect.html">Detect Disease</a></li>
            <li class="{active_weather}"><a href="weather.html">Weather</a></li>
            <li class="{active_market}"><a href="market.html">Market Prices</a></li>
            <li class="{active_assistant}"><a href="assistant.html">AI Assistant</a></li>
            <li class="{active_history}"><a href="history.html">Detection History</a></li>
            <li><a href="#" id="logout-btn">Logout</a></li>
        </ul>
    </div>

    <div class="main-content" id="main-content">
        <div class="header">
            <div class="header-left">
                <button class="hamburger" id="hamburger-btn">
                    &#9776;
                </button>
                <h1>{title}</h1>
            </div>
            <div class="user-info">Welcome, <span id="farmer-name">Loading...</span></div>
        </div>

        <div class="feature-wrapper">
            {content}
        </div>
    </div>

    <script src="js/main.js"></script>
</body>
</html>
"""

pages = {
    "detect": {
        "title": "Detect Disease",
        "content": """
            <div class="card disease-card" style="width: 100%;">
                <div class="card-header">
                    <span class="card-icon">🔬</span>
                    <h2 style="font-family: 'Bitter', serif; font-size: 1.8rem; font-weight: 700; color: #1B4716;">Disease Detection</h2>
                </div>
                <p class="card-description">Upload a plant leaf image for instant AI-powered disease diagnosis</p>
                
                <div class="upload-zone" id="uploadZone">
                   <input type="file" id="imageInput" name="image" accept="image/*" hidden>

                    <div class="upload-content">
                        <div class="upload-icon">📸</div>
                        <p class="upload-text">Click or drag image here</p>
                        <p class="upload-hint">Supports JPG, PNG • Max 10MB</p>
                    </div>
                </div>

                <div id="imagePreview" class="image-preview hidden">
                    <img id="previewImg" src="" alt="Preview">
                    <button class="btn-remove" id="removeImg">✕</button>
                </div>

                <button class="btn-primary" id="detectBtn" disabled>
                    <span class="btn-text">Detect Disease</span>
                    <span class="btn-loader hidden">⏳ Analyzing...</span>
                </button>

                <!-- Results Section -->
                <div id="resultsSection" class="results hidden">
                    <div class="result-header">
                        <h3 style="font-family: 'Bitter', serif; font-size: 1.5rem; color: #1B4716;">Detection Results</h3>
                        <span class="result-time" id="resultTime"></span>
                    </div>
                    
                    <div class="disease-result">
                        <div class="disease-name-section">
                            <span class="severity-badge" id="severityBadge">HIGH</span>
                            <h4 id="diseaseName" style="font-family: 'Bitter', serif; font-size: 1.6rem; color: #1B4716;">Tomato Early Blight</h4>
                        </div>
                        <div class="confidence-meter">
                            <div class="confidence-label">Confidence</div>
                            <div class="confidence-bar">
                                <div class="confidence-fill" id="confidenceFill" style="width: 0%"></div>
                            </div>
                            <div class="confidence-value" id="confidenceValue">0%</div>
                        </div>
                    </div>

                    <div class="treatment-section">
                        <h4>💊 Recommended Treatment</h4>
                        <p id="treatmentText"></p>
                        
                        <h4>⚠ Causes</h4>
                        <p id="causeText"></p>

                        <h4>🧬 Symptoms</h4>
                        <p id="symptomsText"></p>

                        <h4>🛡️ Prevention</h4>
                        <p id="preventionText"></p>

                        <h4>🧪 Chemical Treatment</h4>
                        <p id="chemicalText"></p>
                        
                        <h4>🌿 Organic Alternative</h4>
                        <p id="organicText"></p>
                    </div>

                    <div class="visualization-section">
                        <h4>🔍 AI Visualization (Grad-CAM)</h4>
                        <div class="heatmap-container">
                            <img id="heatmapImg" src="" alt="Grad-CAM Heatmap">
                        </div>
                    </div>
                </div>
            </div>
        """
    },
    "weather": {
        "title": "Weather Forecast",
        "content": """
            <div class="card weather-card" style="width: 100%;">
                <div class="card-header">
                    <span class="card-icon">🌤️</span>
                    <h2 style="font-family: 'Bitter', serif; font-size: 1.8rem; font-weight: 700; color: #1B4716;">Weather Advisory</h2>
                </div>
                <p class="card-description">Real-time weather data and farming recommendations</p>
                
                <div class="location-input">
                    <input type="text" id="locationInput" placeholder="Enter location (e.g., Bangalore)" value="Bangalore">
                    <button class="btn-secondary" id="weatherBtn">Get Weather</button>
                </div>

                <div id="weatherData" class="weather-data hidden">
                    <div class="weather-current">
                        <div class="temp-display">
                            <span class="temp-value" id="tempValue">28</span>
                            <span class="temp-unit">°C</span>
                        </div>
                        <div class="weather-info">
                            <p class="weather-condition" id="weatherCondition">Partly Cloudy</p>
                            <p class="weather-location" id="weatherLocation">Bangalore, Karnataka</p>
                        </div>
                    </div>

                    <div class="weather-stats">
                        <div class="stat-item">
                            <span class="stat-icon">💧</span>
                            <span class="stat-label">Humidity</span>
                            <span class="stat-value" id="humidity">65%</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-icon">💨</span>
                            <span class="stat-label">Wind</span>
                            <span class="stat-value" id="wind">12 km/h</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-icon">☀️</span>
                            <span class="stat-label">UV Index</span>
                            <span class="stat-value" id="uvIndex">7</span>
                        </div>
                    </div>

                    <div class="agricultural-advisory">
                        <h4>🌾 Agricultural Advisory</h4>
                        <div class="advisory-item">
                            <strong>Irrigation:</strong>
                            <span id="irrigationAdv">Moderate irrigation recommended</span>
                        </div>
                        <div class="advisory-item">
                            <strong>Disease Risk:</strong>
                            <span id="diseaseRisk">Monitor for fungal diseases</span>
                        </div>
                        <div class="advisory-item">
                            <strong>Spraying:</strong>
                            <span id="sprayingAdv">Good conditions for application</span>
                        </div>
                    </div>
                </div>
            </div>
        """
    },
    "market": {
        "title": "Market Prices",
        "content": """
<div class="card market-card" style="width: 100%;">
    <div class="card-header">
        <span class="card-icon">💰</span>
        <h2 style="font-family: 'Bitter', serif; font-size: 1.8rem; font-weight: 700; color: #1B4716;">Market Intelligence</h2>
    </div>

    <p class="card-description">
        Live mandi prices from across India
    </p>

    <div class="crop-selector">
        <select id="cropSelect" class="crop-select">
            <option value="tomato">Tomato</option>
            <option value="potato">Potato</option>
            <option value="onion">Onion</option>
            <option value="chili">Chilli</option>
            <option value="rice">Rice</option>
        </select>

        <button class="btn-secondary" id="marketBtn">
            Get Prices
        </button>
    </div>

    <div id="marketData" class="market-data hidden">

        <div class="price-display">
            <div class="current-price">
                <span class="price-label">Current Price</span>
                <span class="price-value">
                    ₹<span id="currentPrice">--</span>
                </span>
                <span class="price-unit">/quintal</span>
            </div>

            <div class="price-trend">
                <span class="trend-badge trend-up" id="trendBadge">
                    ↑ <span id="trendPercent">--</span>%
                </span>
            </div>
        </div>

        <p id="mandiName" style="margin-top:6px;font-weight:600;color:#555">
            Mandi: --
        </p>

        <div class="price-range">
            <div class="range-item">
                <span>Min</span>
                <strong>₹<span id="minPrice">--</span></strong>
            </div>

            <div class="range-item">
                <span>Avg</span>
                <strong>₹<span id="avgPrice">--</span></strong>
            </div>

            <div class="range-item">
                <span>Max</span>
                <strong>₹<span id="maxPrice">--</span></strong>
            </div>
        </div>

        <div class="market-recommendation">
            <div class="recommendation-header">
                <span class="rec-badge" id="actionBadge">--</span>
                <h4>Recommendation</h4>
            </div>
            <p id="recommendationText">Loading...</p>
        </div>

        <div class="top-markets">
            <h4>🏪 Top Mandis</h4>
            <div class="market-list" id="marketList">
            </div>
        </div>

    </div>
</div>
        """
    },
    "assistant": {
        "title": "AI Assistant",
        "content": """
            <div class="card chat-card" style="width: 100%;">
                <div class="card-header">
                    <span class="card-icon">🤖</span>
                    <h2 style="font-family: 'Bitter', serif; font-size: 1.8rem; font-weight: 700; color: #1B4716;">AI Farm Assistant</h2>
                </div>
                <p class="card-description">Ask me anything about farming, diseases, or crop management</p>
                
                <div class="chat-container" id="chatContainer">
                    <div class="chat-welcome">
                        <div class="welcome-icon">👋</div>
                        <h3>Hello, Farmer!</h3>
                        <p>I'm your AI farming assistant. Ask me anything!</p>
                        <div class="suggestion-chips">
                            <button class="chip" data-query="How to prevent fungal diseases?">Prevent Diseases</button>
                            <button class="chip" data-query="When is the best time to sell crops?">Market Timing</button>
                            <button class="chip" data-query="What are organic pest control methods?">Organic Methods</button>
                        </div>
                    </div>
                    <div class="chat-messages" id="chatMessages"></div>
                </div>

                <div class="chat-input-container">
                    <input type="text" id="chatInput" placeholder="Type your question here..." class="chat-input">
                    <button class="btn-send" id="sendBtn">
                        <span style="color:white; font-size: 0.95rem; font-weight:600;">Send</span>
                        <span class="send-icon">📤</span>
                    </button>
                </div>
            </div>
        """
    }
}

for key, data in pages.items():
    with open(f"d:\\Agro Sense\\Agro-sense-main\\frontend\\{key}.html", "w", encoding="utf-8") as f:
        html = template.format(
            title=data["title"],
            content=data["content"],
            active_detect="active" if key == "detect" else "",
            active_weather="active" if key == "weather" else "",
            active_market="active" if key == "market" else "",
            active_assistant="active" if key == "assistant" else "",
            active_history="",
        )
        f.write(html)
