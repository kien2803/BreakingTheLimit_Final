// BREAKING THE LIMITS - MAIN JAVASCRIPT

const API_BASE_URL = 'http://localhost:5000/api';

// Utility Functions
function isLoggedIn() {
    return localStorage.getItem('authToken') !== null;
}

function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    window.location.href = 'index.html';
}

// Modal Functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// Alert Functions
function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        padding: 1rem 2rem;
        background: ${type === 'success' ? '#4A7C59' : type === 'error' ? '#C97676' : '#E4A972'};
        color: white;
        border-radius: 10px;
        z-index: 9999;
        animation: slideIn 0.3s ease-out;
    `;
    alert.textContent = message;
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => alert.remove(), 300);
    }, 3000);
}

// Loading Functions
function showLoading(message = 'Đang xử lý...') {
    let overlay = document.getElementById('loadingOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loadingOverlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div>
                <div class="loading-spinner"></div>
                <p style="margin-top: 1rem; color: #666;">${message}</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }
    overlay.classList.add('active');
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.remove('active');
}

// Scroll Reveal
function initScrollReveal() {
    const reveals = document.querySelectorAll('.scroll-reveal');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, { threshold: 0.1 });
    
    reveals.forEach(el => observer.observe(el));
}

// Date Formatting
function formatDate(date, format = 'dd/mm/yyyy') {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    
    if (format === 'relative') {
        const diff = Date.now() - d.getTime();
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (minutes < 1) return 'Vừa xong';
        if (minutes < 60) return `${minutes} phút trước`;
        if (hours < 24) return `${hours} giờ trước`;
        if (days < 7) return `${days} ngày trước`;
    }
    
    return `${day}/${month}/${year}`;
}

// Validation
function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Confetti Effect
function createConfetti() {
    const colors = ['#4A7C59', '#CFE6D1', '#E4A972'];
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
            position: fixed;
            width: 10px;
            height: 10px;
            background: ${colors[Math.floor(Math.random() * colors.length)]};
            left: ${Math.random() * 100}vw;
            top: -10px;
            border-radius: 50%;
            animation: confetti-fall 3s linear forwards;
            z-index: 9999;
        `;
        document.body.appendChild(confetti);
        setTimeout(() => confetti.remove(), 3000);
    }
}

// Storage Helpers
function saveToLocalStorage(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

function getFromLocalStorage(key) {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
}

// Export to global
window.BTL = {
    isLoggedIn,
    logout,
    openModal,
    closeModal,
    showAlert,
    showLoading,
    hideLoading,
    formatDate,
    validateEmail,
    createConfetti,
    saveToLocalStorage,
    getFromLocalStorage
};

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    initScrollReveal();
    
    // Mobile menu
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    if (menuBtn) {
        menuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }
});

console.log('Breaking The Limits loaded ✓');