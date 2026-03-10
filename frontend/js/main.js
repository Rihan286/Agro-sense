// ===== Configuration =====
const API_BASE_URL = 'http://localhost:5000/api';

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
uploadZone.addEventListener('click', () => imageInput.click());

imageInput.addEventListener('change', (e) => {
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

removeImgBtn.addEventListener('click', () => {
    selectedImage = null;
    imageInput.value = '';
    imagePreview.classList.add('hidden');
    uploadZone.style.display = 'block';
    detectBtn.disabled = true;
    resultsSection.classList.add('hidden');
});

// ===== Detect Disease =====
detectBtn.addEventListener('click', async () => {
    if (!selectedImage) return;

    showLoading(detectBtn);

    try {
        const formData = new FormData();
        formData.append('image', selectedImage);

        const res = await fetch(`${API_BASE_URL}/detect-disease`, {
            method: 'POST',
            body: formData
        });

        const data = await res.json();

        if (!data.success) throw new Error('Detection failed');

        showResults(data.prediction);

    } catch (err) {
        alert('Disease detection failed');
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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ disease: prediction.disease })
    });

    const advisoryData = await advisoryRes.json();

    const fullText = advisoryData.advisory || "";

function extract(section) {
    const regex = new RegExp(section + ":(.*?)(?=\\n[A-Z ]+:|$)", "s");
    const match = fullText.match(regex);
    return match ? match[1].trim() : "";
}

document.getElementById('treatmentText').textContent = extract("INTRO") || fullText;
document.getElementById('causeText').textContent = extract("CAUSES");
document.getElementById('symptomsText').textContent = extract("SYMPTOMS");
document.getElementById('preventionText').textContent = extract("PREVENTION");
document.getElementById('chemicalText').textContent = extract("CHEMICAL");
document.getElementById('organicText').textContent = extract("ORGANIC");
}

// ===== Weather =====
weatherBtn.addEventListener('click', async () => {

    const location = locationInput.value.trim();
    if (!location) return;

    try {
        const res = await fetch(`${API_BASE_URL}/weather?location=${location}`);
        const data = await res.json();

        if (!data.success) throw new Error("Weather failed");

        weatherData.classList.remove('hidden');

        document.getElementById('tempValue').textContent =
            Math.round(data.data.current.temperature);

        document.getElementById('weatherCondition').textContent =
            data.data.current.conditions;

        document.getElementById('weatherLocation').textContent =
            data.data.location;

    } catch (err) {
        console.error(err);
        alert("Weather error");
    }
});

// ===== Chat (simple advisory reuse) =====
sendBtn.addEventListener('click', async () => {
    const message = chatInput.value.trim();
    if (!message) return;

    // show user message
    chatMessages.innerHTML += `<div class="message user">${message}</div>`;
    chatInput.value = "";

    const res = await fetch(`${API_BASE_URL}/advisory`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
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

marketBtn.addEventListener("click", async () => {
    const crop = cropSelect.value;

    try {
        const res = await fetch(`http://localhost:5000/api/market-prices?crop=${crop}`);
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