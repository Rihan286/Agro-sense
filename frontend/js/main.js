// ===== AgroSense — Main JS v2.0 =====
// Auth, layout, dark mode, notifications, sidebar

// ===== Configuration =====
const API_BASE_URL = 'http://localhost:5000/api';

// ===== Auth Check =====
const token = localStorage.getItem('agrosense_token');
if (!token) {
    window.location.href = 'login.html';
}

function getAuthHeaders(isFileUpload = false) {
    const headers = { 'Authorization': `Bearer ${token}` };
    if (!isFileUpload) headers['Content-Type'] = 'application/json';
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

// ===== Logout =====
function performLogout(e) {
    if(e) e.preventDefault();
    localStorage.removeItem('agrosense_token');
    localStorage.removeItem('agrosense_user');
    document.body.style.transition = 'opacity 0.4s ease';
    document.body.style.opacity = '0';
    setTimeout(() => window.location.href = 'index.html', 400);
}

const logoutBtn = document.getElementById('logout-btn');
if (logoutBtn) logoutBtn.addEventListener('click', performLogout);
const sidebarLogoutBtn = document.getElementById('sidebar-logout-btn');
if (sidebarLogoutBtn) sidebarLogoutBtn.addEventListener('click', performLogout);
const ddLogoutBtn = document.getElementById('dropdown-logout');
if (ddLogoutBtn) ddLogoutBtn.addEventListener('click', performLogout);

// ===== Dropdown Logic =====
const userMenuBtn = document.getElementById('user-menu-btn');
const userDropdown = document.getElementById('user-dropdown');
if (userMenuBtn && userDropdown) {
    userMenuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.classList.toggle('show');
    });
    document.addEventListener('click', (e) => {
        if (!userDropdown.contains(e.target)) {
            userDropdown.classList.remove('show');
        }
    });
}

// ===== Sidebar Toggle =====
const globHamburgerBtn = document.getElementById('hamburger-btn');
const globSidebar = document.getElementById('sidebar');
const globMainContent = document.getElementById('main-content');
const sidebarOverlay = document.getElementById('sidebar-overlay');

if (globHamburgerBtn) {
    globHamburgerBtn.addEventListener('click', () => {
        if (globSidebar) globSidebar.classList.toggle('active');
        if (sidebarOverlay) sidebarOverlay.classList.toggle('active');
    });
}

if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', () => {
        if (globSidebar) globSidebar.classList.remove('active');
        sidebarOverlay.classList.remove('active');
    });
}

// ===== Dark Mode =====
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('agrosense_theme', theme);
    if (themeIcon) {
        // Re-render feather icon
        themeIcon.setAttribute('data-feather', theme === 'dark' ? 'sun' : 'moon');
        if (typeof feather !== 'undefined') feather.replace();
    }
}

// Init theme
const savedTheme = localStorage.getItem('agrosense_theme') || 'light';
setTheme(savedTheme);

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        setTheme(current === 'dark' ? 'light' : 'dark');
    });
}

// ===== Notifications =====
const notifBtn = document.getElementById('notif-btn');
const notifPanel = document.getElementById('notif-panel');
const notifList = document.getElementById('notif-list');
const notifCount = document.getElementById('notif-count');
const markAllRead = document.getElementById('mark-all-read');

const notifications = [
    {
        type: 'weather',
        icon: '🌧️',
        title: 'Rain expected tomorrow in your area',
        time: '10 min ago',
        unread: true
    },
    {
        type: 'disease',
        icon: '⚠️',
        title: 'High humidity — risk of fungal disease',
        time: '1 hour ago',
        unread: true
    },
    {
        type: 'market',
        icon: '📈',
        title: 'Tomato prices increased by 5%',
        time: '3 hours ago',
        unread: true
    },
    {
        type: 'weather',
        icon: '🌡️',
        title: 'Temperature drop expected this weekend',
        time: '5 hours ago',
        unread: false
    },
    {
        type: 'market',
        icon: '📉',
        title: 'Onion prices down 2% — hold selling',
        time: 'Yesterday',
        unread: false
    }
];

function renderNotifications() {
    if (!notifList) return;
    notifList.innerHTML = notifications.map(n => `
        <div class="notification-item ${n.unread ? 'unread' : ''}">
            <div class="notif-icon ${n.type}">${n.icon}</div>
            <div class="notif-content">
                <div class="notif-title">${n.title}</div>
                <div class="notif-time">${n.time}</div>
            </div>
        </div>
    `).join('');

    const unreadCount = notifications.filter(n => n.unread).length;
    if (notifCount) {
        notifCount.textContent = unreadCount;
        notifCount.style.display = unreadCount > 0 ? 'flex' : 'none';
    }
}

if (notifBtn && notifPanel) {
    notifBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        notifPanel.classList.toggle('show');
        // Close user dropdown if open
        if (userDropdown) userDropdown.classList.remove('show');
    });

    document.addEventListener('click', (e) => {
        if (!notifPanel.contains(e.target) && !notifBtn.contains(e.target)) {
            notifPanel.classList.remove('show');
        }
    });
}

if (markAllRead) {
    markAllRead.addEventListener('click', () => {
        notifications.forEach(n => n.unread = false);
        renderNotifications();
    });
}

renderNotifications();

// ===== Utilities =====
function showLoading(button, text = 'Loading...') {
    button.disabled = true;
    const btnText = button.querySelector('.btn-text');
    const btnLoader = button.querySelector('.btn-loader');
    if (btnText) btnText.classList.add('hidden');
    if (btnLoader) btnLoader.classList.remove('hidden');
}

function hideLoading(button) {
    button.disabled = false;
    const btnText = button.querySelector('.btn-text');
    const btnLoader = button.querySelector('.btn-loader');
    if (btnText) btnText.classList.remove('hidden');
    if (btnLoader) btnLoader.classList.add('hidden');
}

function formatTime() {
    return new Date().toLocaleTimeString();
}