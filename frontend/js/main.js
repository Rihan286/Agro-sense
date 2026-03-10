// ===== Configuration =====
const API_BASE_URL = 'http://localhost:5000/api';

// ===== Auth Check =====
const token = localStorage.getItem('agrosense_token');
if (!token) {
    window.location.href = 'login.html';
}

// Add token to headers helper
function getAuthHeaders(isFileUpload = false) {
    const headers = {
        'Authorization': `Bearer ${token}`
    };
    if (!isFileUpload) {
        headers['Content-Type'] = 'application/json';
    }
    return headers;
}


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
    if (globSidebar) globSidebar.classList.toggle('active');
    
    // Only expand main content spacing on desktop, mobile overlays it natively
    if (window.innerWidth > 768) {
        if (globMainContent) globMainContent.classList.toggle('expanded');
    }
});

// ===== DOM Elements =====
const uploadZone = document.getElementById('uploadZone');
const imageInput = document.getElementById('imageInput');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const removeImgBtn = document.getElementById('removeImg');
const detectBtn = document.getElementById('detectBtn');
const resultsSection = document.getElementById('resultsSection');

const weatherBtn = document.getElementById('weatherBtn');
const locationInput = document.getElementById('locationInput');
const weatherData = document.getElementById('weatherData');

const marketData = document.getElementById('marketData');

const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');
const chatContainer = document.getElementById('chatContainer');

// ===== Global State =====
let selectedImage = null;

// ===== Utilities =====
function showLoading(button, text = 'Loading...') {
    button.disabled = true;
    button.querySelector('.btn-text')?.classList.add('hidden');
    button.querySelector('.btn-loader')?.classList.remove('hidden');
}

function hideLoading(button) {
    button.disabled = false;
    button.querySelector('.btn-text')?.classList.remove('hidden');
    button.querySelector('.btn-loader')?.classList.add('hidden');
}

function formatTime() {
    return new Date().toLocaleTimeString();
}

// ===== Image Upload =====
if (uploadZone) uploadZone.addEventListener('click', () => imageInput.click());

if (imageInput) imageInput.addEventListener('change', (e) => {
    selectedImage = e.target.files[0];
    if (!selectedImage) return;

    const reader = new FileReader();
    reader.onload = e => {
        previewImg.src = e.target.result;
        uploadZone.style.display = 'none';
        imagePreview.classList.remove('hidden');
        detectBtn.disabled = false;
    };
    reader.readAsDataURL(selectedImage);
});

if (removeImgBtn) removeImgBtn.addEventListener('click', () => {
    selectedImage = null;
    imageInput.value = '';
    imagePreview.classList.add('hidden');
    uploadZone.style.display = 'block';
    detectBtn.disabled = true;
    resultsSection.classList.add('hidden');
});

// ===== Detect Disease =====
if (detectBtn) detectBtn.addEventListener('click', async () => {
    if (!selectedImage) return;

    showLoading(detectBtn);

    try {
        const formData = new FormData();
        formData.append('image', selectedImage);

        const res = await fetch(`${API_BASE_URL}/disease/detect`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });

        if (res.status === 401 || res.status === 422) {
            localStorage.removeItem('agrosense_token');
            localStorage.removeItem('agrosense_user');
            alert('Your active session has expired (Server restarted). Please log in again to continue!');
            window.location.href = 'login.html';
            return;
        }

        if (res.status === 413) {
            alert('Image is too large! Please upload an image smaller than 16MB.');
            return;
        }

        let data;
        try {
            data = await res.json();
        } catch (parseErr) {
            throw new Error('Server returned an invalid response (Status: ' + res.status + ')');
        }

        if (!res.ok || !data.success) {
            throw new Error(data.error || data.msg || 'Detection failed');
        }

        showResults(data.prediction);

    } catch (err) {
        alert('Disease detection failed: ' + err.message);
        console.error(err);
    } finally {
        hideLoading(detectBtn);
    }
});

// ===== Display Results + Gemini Advisory =====
async function showResults(prediction) {
    resultsSection.classList.remove('hidden');

    document.getElementById('resultTime').textContent = formatTime();
    document.getElementById('diseaseName').textContent = prediction.disease;
    document.getElementById('severityBadge').textContent = 'DETECTED';

    document.getElementById('confidenceFill').style.width = prediction.confidence + '%';
    document.getElementById('confidenceValue').textContent = prediction.confidence + '%';

    // Call Gemini advisory
    const advisoryRes = await fetch(`${API_BASE_URL}/advisory`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ disease: prediction.disease })
    });

    const advisoryData = await advisoryRes.json();

    const fullText = advisoryData.advisory || "";

function extract(section) {
    const regex = new RegExp(section + ":(.*?)(?=\\n[A-Z ]+:|$)", "s");
    const match = fullText.match(regex);
    return match ? match[1].trim() : "";
}
function cleanMarkdown(text) {
    if (!text) return "";
    // Replace markdown bold **text** with HTML <strong>text</strong>
    return text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
}

document.getElementById('treatmentText').innerHTML = cleanMarkdown(extract("INTRO") || fullText);
document.getElementById('causeText').innerHTML = cleanMarkdown(extract("CAUSES"));
document.getElementById('symptomsText').innerHTML = cleanMarkdown(extract("SYMPTOMS"));
document.getElementById('preventionText').innerHTML = cleanMarkdown(extract("PREVENTION"));
document.getElementById('chemicalText').innerHTML = cleanMarkdown(extract("CHEMICAL"));
document.getElementById('organicText').innerHTML = cleanMarkdown(extract("ORGANIC"));
}

// ===== Weather =====
if (weatherBtn) weatherBtn.addEventListener('click', async () => {

    const location = locationInput.value.trim();
    if (!location) return;

    try {
        const res = await fetch(`${API_BASE_URL}/weather?location=${location}`, {
            headers: getAuthHeaders()
        });
        const data = await res.json();

        if (!data.success) throw new Error("Weather failed");

        weatherData.classList.remove('hidden');

        document.getElementById('tempValue').textContent =
            Math.round(data.data.current.temperature);

        document.getElementById('weatherCondition').textContent =
            data.data.current.conditions;

        document.getElementById('weatherLocation').textContent =
            data.data.location;

        const humidity = data.data.current.humidity;
        const windSpeed = data.data.current.wind_speed;
        const temp = data.data.current.temperature;
        const condition = data.data.current.conditions.toLowerCase();

        // Dynamically update the DOM Stats elements
        const humidityEl = document.getElementById('humidity');
        const windEl = document.getElementById('wind');
        const uvEl = document.getElementById('uvIndex');

        if (humidityEl) humidityEl.textContent = `${humidity}%`;
        if (windEl) windEl.textContent = `${windSpeed} km/h`;
        if (uvEl) uvEl.textContent = data.data.current.uv_index;

        // Agriculture Advisory Logic
        let irrigation = "Moderate irrigation recommended";
        let disease = "Standard monitoring";
        let spraying = "Good conditions for application";

        if (temp > 35) {
            irrigation = "High temperature: increase irrigation significantly";
        } else if (condition.includes('rain') || condition.includes('drizzle')) {
            irrigation = "Rain expected: pause irrigation";
        }

        if (humidity > 70) {
            disease = "High humidity: high risk of fungal diseases (Monitor closely)";
        } else if (humidity < 30) {
            disease = "Low humidity: watch out for mites and pests";
        }

        if (windSpeed > 20) {
            spraying = "High wind: Avoid spraying chemicals / fertilizers";
        } else if (condition.includes('rain')) {
            spraying = "Rain expected: Avoid spraying as it will wash off";
        }

        const irrEl = document.getElementById('irrigationAdv');
        const disEl = document.getElementById('diseaseRisk');
        const sprayEl = document.getElementById('sprayingAdv');

        if (irrEl) irrEl.textContent = irrigation;
        if (disEl) disEl.textContent = disease;
        if (sprayEl) sprayEl.textContent = spraying;

    } catch (err) {
        console.error(err);
        alert("Weather error");
    }
});

// ===== Chat (simple advisory reuse) =====
if (sendBtn) sendBtn.addEventListener('click', async () => {
    const message = chatInput.value.trim();
    if (!message) return;

    // show user message
    chatMessages.innerHTML += `<div class="message user">${message}</div>`;
    chatInput.value = "";

    const res = await fetch(`${API_BASE_URL}/advisory`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ disease: message })
    });

    const data = await res.json();

    // show bot response (reply OR advisory)
    const botText = data.reply || data.advisory || "No response";
    chatMessages.innerHTML += `<div class="message assistant">${botText}</div>`;
});


// MARKET BUTTON
const marketBtn = document.getElementById("marketBtn");
const cropSelect = document.getElementById("cropSelect");

if (marketBtn) marketBtn.addEventListener("click", async () => {
    const crop = cropSelect.value;

    try {
        const res = await fetch(`${API_BASE_URL}/market-prices?crop=${crop}`, {
            headers: getAuthHeaders()
        });
        const data = await res.json();

        if (!data.success) throw new Error("No data");

        const market = data.data;

        // show card
        document.getElementById("marketData").classList.remove("hidden");

        // price
        document.getElementById("currentPrice").textContent = market.price;
        document.getElementById("minPrice").textContent = market.min_price;
        document.getElementById("maxPrice").textContent = market.max_price;
        document.getElementById("avgPrice").textContent = market.avg_price;

        // mandi name
        document.getElementById("mandiName").textContent = market.market;

        // recommendation
        document.getElementById("actionBadge").textContent = market.recommendation.action;
        document.getElementById("recommendationText").textContent = market.recommendation.reason;

        // top markets
        const list = document.getElementById("marketList");
        list.innerHTML = "";

        market.top_markets.forEach(m => {
            list.innerHTML += `
                <div class="market-item">
                    ${m.name} — ₹${m.price}
                </div>
            `;
        });

    } catch (err) {
        console.error(err);
        alert("Market fetch failed");
    }
});

// HISTORY LOGIC
const historyTable = document.getElementById('history-table');
if (historyTable) {
    async function fetchHistory() {
        const statusMsg = document.getElementById('status-message');
        const tbody = document.getElementById('history-body');

        try {
            const response = await fetch(`${API_BASE_URL}/disease/history`, {
                headers: getAuthHeaders()
            });

            const data = await response.json();

            if (response.ok && data.success) {
                if (data.history.length === 0) {
                    statusMsg.textContent = "No detection history found.";
                } else {
                    statusMsg.style.display = 'none';
                    historyTable.style.display = 'table';
                    
                    data.history.forEach(item => {
                        const tr = document.createElement('tr');
                        
                        // Format Date
                        const dateObj = new Date(item.timestamp);
                        const dateStr = dateObj.toLocaleString();
                        
                        // Confidence Color
                        let confClass = 'confidence-high';
                        if (item.confidence < 70) confClass = 'confidence-low';
                        else if (item.confidence < 85) confClass = 'confidence-med';

                        tr.innerHTML = `
                            <td>${dateStr}</td>
                            <td><span style="text-transform: capitalize;">${item.crop || 'Unknown'}</span></td>
                            <td>${item.disease}</td>
                            <td class="${confClass}">${item.confidence}%</td>
                            <td>${item.image_path ? 'Uploaded Image' : 'N/A'}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                }
            } else {
                statusMsg.textContent = data.error || 'Failed to load history';
                statusMsg.className = 'error';
            }
        } catch (err) {
            statusMsg.textContent = 'Connection error';
            statusMsg.className = 'error';
        }
    }
    fetchHistory();
}