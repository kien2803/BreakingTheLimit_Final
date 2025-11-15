// ===== FAMILY PAGE JAVASCRIPT (UPDATED) =====

let currentRole = null;
let selectedChildId = null;
let emotionChartInstance = null;

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication
    if (!BTL.isLoggedIn()) {
        window.location.href = 'auth.html';
        return;
    }

    // Get current user
    const user = BTL.getCurrentUser();
    if (!user) {
        window.location.href = 'auth.html';
        return;
    }

    // Auto select role based on user
    currentRole = user.role;
    
    // Or check URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const roleParam = urlParams.get('role');
    if (roleParam) {
        currentRole = roleParam;
    }

    // Show appropriate view
    document.getElementById('roleSelector').style.display = 'none';
    
    if (currentRole === 'parent') {
        document.getElementById('parentView').classList.remove('hidden');
        loadChildrenList();
    } else if (currentRole === 'student') {
        document.getElementById('studentView').classList.remove('hidden');
        loadStudentData();
    } else {
        // If role is neither, show selector
        document.getElementById('roleSelector').style.display = 'block';
    }
});

// ===== ROLE SELECTION (Fallback) =====
function selectRole(role) {
    currentRole = role;
    document.getElementById('roleSelector').classList.add('hidden');
    
    if (role === 'parent') {
        document.getElementById('parentView').classList.remove('hidden');
        loadChildrenList();
    } else {
        document.getElementById('studentView').classList.remove('hidden');
        loadStudentData();
    }
}

// ===== PARENT VIEW FUNCTIONS =====

async function loadChildrenList() {
    BTL.showLoading('Đang tải danh sách...');
    
    try {
        await MockAPI.delay(1000);
        
        const mockChildren = [
            {
                id: 1,
                name: 'Nguyễn Văn An',
                avatar: '👦',
                age: 16,
                lastActive: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
                wellnessScore: 78,
                recentMood: 'happy',
                alerts: 0
            },
            {
                id: 2,
                name: 'Nguyễn Thị Bình',
                avatar: '👧',
                age: 15,
                lastActive: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
                wellnessScore: 65,
                recentMood: 'neutral',
                alerts: 1
            }
        ];
        
        renderChildrenGrid(mockChildren);
    } catch (error) {
        BTL.showAlert('Không thể tải danh sách con', 'error');
    } finally {
        BTL.hideLoading();
    }
}

function renderChildrenGrid(children) {
    const grid = document.getElementById('childrenGrid');
    
    if (children.length === 0) {
        grid.innerHTML = '<p class="empty-state">Chưa có con nào được kết nối. Nhấn "Kết nối con" để bắt đầu.</p>';
        return;
    }
    
    grid.innerHTML = children.map(child => `
        <div class="child-card" onclick="selectChild(${child.id})">
            <div class="child-avatar">${child.avatar}</div>
            <div class="child-info">
                <h3>${child.name}</h3>
                <p>${child.age} tuổi</p>
                <div class="child-status">
                    <span class="status-badge ${child.wellnessScore >= 70 ? 'good' : child.wellnessScore >= 50 ? 'moderate' : 'concern'}">
                        ${child.wellnessScore}/100
                    </span>
                    <span class="mood-indicator">${getMoodEmoji(child.recentMood)}</span>
                </div>
                <p class="last-active">
                    ${BTL.formatDate(child.lastActive, 'relative')}
                </p>
                ${child.alerts > 0 ? `
                    <div class="alert-badge">
                        ⚠️ ${child.alerts} cảnh báo
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

function getMoodEmoji(mood) {
    const moods = {
        'very-happy': '😄',
        'happy': '😊',
        'neutral': '😐',
        'sad': '😞',
        'very-sad': '😢',
        'angry': '😡'
    };
    return moods[mood] || '😐';
}

async function selectChild(childId) {
    selectedChildId = childId;
    document.querySelector('.children-section').classList.add('hidden');
    document.getElementById('childDashboard').classList.remove('hidden');
    
    await loadChildDashboard(childId);
}

function backToChildren() {
    document.querySelector('.children-section').classList.remove('hidden');
    document.getElementById('childDashboard').classList.add('hidden');
    selectedChildId = null;
}

async function loadChildDashboard(childId) {
    BTL.showLoading('Đang tải dữ liệu...');
    
    try {
        await MockAPI.delay(1000);
        
        const childData = {
            name: 'Nguyễn Văn An',
            lastActive: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
            wellnessScore: 78,
            trend: '+5',
            journalCount: 12,
            streakDays: 7,
            moodVariation: 'Ổn định',
            emotionData: {
                positive: [65, 70, 68, 72, 75, 73, 78],
                neutral: [25, 20, 22, 18, 15, 20, 15],
                negative: [10, 10, 10, 10, 10, 7, 7]
            },
            alerts: [
                {
                    type: 'suggestion',
                    message: 'Con có vẻ hơi căng thẳng những ngày qua. Hãy rủ con đi dạo hoặc trò chuyện nhẹ nhàng.'
                }
            ]
        };
        
        document.getElementById('childName').textContent = childData.name;
        document.getElementById('childLastActive').textContent = 
            `Hoạt động lần cuối: ${BTL.formatDate(childData.lastActive, 'relative')}`;
        
        document.getElementById('wellnessScoreParent').textContent = childData.wellnessScore;
        document.getElementById('wellnessTrend').innerHTML = 
            `<span style="color: ${childData.trend.startsWith('+') ? '#4A7C59' : '#C97676'}">
                ${childData.trend} điểm so với tuần trước
            </span>`;
        
        document.getElementById('journalCount').textContent = childData.journalCount;
        document.getElementById('streakDays').textContent = childData.streakDays;
        document.getElementById('moodVariation').textContent = childData.moodVariation;
        
        renderAlerts(childData.alerts);
        renderEmotionChart(childData.emotionData);
        
    } catch (error) {
        BTL.showAlert('Không thể tải dữ liệu', 'error');
    } finally {
        BTL.hideLoading();
    }
}

function renderAlerts(alerts) {
    const alertsList = document.getElementById('alertsList');
    
    if (alerts.length === 0) {
        alertsList.innerHTML = '<p class="empty-state">✓ Không có cảnh báo</p>';
        return;
    }
    
    alertsList.innerHTML = alerts.map(alert => `
        <div class="alert-item ${alert.type}">
            <span class="alert-icon">${alert.type === 'warning' ? '⚠️' : '💡'}</span>
            <p>${alert.message}</p>
        </div>
    `).join('');
}

function renderEmotionChart(data) {
    const canvas = document.getElementById('emotionChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    if (emotionChartInstance) {
        emotionChartInstance.destroy();
    }
    
    const days = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN'];
    const maxValue = 100;
    const padding = 40;
    const chartWidth = canvas.width - padding * 2;
    const chartHeight = canvas.height - padding * 2;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw axes
    ctx.strokeStyle = '#ddd';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.stroke();
    
    // Draw lines
    const colors = {
        positive: '#4A7C59',
        neutral: '#E4A972',
        negative: '#C97676'
    };
    
    Object.entries(data).forEach(([key, values]) => {
        ctx.strokeStyle = colors[key];
        ctx.lineWidth = 3;
        ctx.beginPath();
        
        values.forEach((value, index) => {
            const x = padding + (chartWidth / (values.length - 1)) * index;
            const y = canvas.height - padding - (value / maxValue) * chartHeight;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        
        ctx.stroke();
        
        // Draw points
        values.forEach((value, index) => {
            const x = padding + (chartWidth / (values.length - 1)) * index;
            const y = canvas.height - padding - (value / maxValue) * chartHeight;
            
            ctx.fillStyle = colors[key];
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fill();
        });
    });
    
    // Draw day labels
    ctx.fillStyle = '#666';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    days.forEach((day, index) => {
        const x = padding + (chartWidth / (days.length - 1)) * index;
        ctx.fillText(day, x, canvas.height - 15);
    });
    
    // Draw legend
    const legends = [
        { color: colors.positive, label: 'Tích cực' },
        { color: colors.neutral, label: 'Trung tính' },
        { color: colors.negative, label: 'Tiêu cực' }
    ];
    
    legends.forEach((legend, index) => {
        const x = padding + index * 100;
        const y = 20;
        
        ctx.fillStyle = legend.color;
        ctx.fillRect(x, y, 15, 15);
        
        ctx.fillStyle = '#333';
        ctx.textAlign = 'left';
        ctx.fillText(legend.label, x + 20, y + 12);
    });
}

async function sendEncouragement() {
    const message = document.getElementById('encouragementText').value.trim();
    
    if (!message) {
        BTL.showAlert('Vui lòng nhập tin nhắn', 'warning');
        return;
    }
    
    BTL.showLoading('Đang gửi...');
    
    try {
        await MockAPI.delay(1000);
        BTL.showAlert('Đã gửi tin nhắn động viên!', 'success');
        document.getElementById('encouragementText').value = '';
        BTL.createConfetti();
    } catch (error) {
        BTL.showAlert('Không thể gửi tin nhắn', 'error');
    } finally {
        BTL.hideLoading();
    }
}

async function linkChild() {
    const email = document.getElementById('childEmail').value.trim();
    const code = document.getElementById('verificationCode').value.trim();
    
    if (!email) {
        BTL.showAlert('Vui lòng nhập email', 'warning');
        return;
    }
    
    if (!BTL.validateEmail(email)) {
        BTL.showAlert('Email không hợp lệ', 'error');
        return;
    }
    
    BTL.showLoading('Đang gửi yêu cầu...');
    
    try {
        await MockAPI.delay(1000);
        BTL.showAlert('Đã gửi yêu cầu kết nối!', 'success');
        BTL.closeModal('linkChildModal');
        await loadChildrenList();
    } catch (error) {
        BTL.showAlert('Không thể gửi yêu cầu', 'error');
    } finally {
        BTL.hideLoading();
    }
}

// ===== STUDENT VIEW FUNCTIONS =====

async function loadStudentData() {
    BTL.showLoading('Đang tải dữ liệu...');
    
    try {
        await MockAPI.delay(1000);
        
        const mockParents = [
            {
                id: 1,
                name: 'Nguyễn Văn Cha',
                email: 'cha@example.com',
                relationship: 'Cha',
                connectedDate: '2024-01-15'
            },
            {
                id: 2,
                name: 'Trần Thị Mẹ',
                email: 'me@example.com',
                relationship: 'Mẹ',
                connectedDate: '2024-01-15'
            }
        ];
        
        renderConnectedParents(mockParents);
        
        const mockMessages = [
            {
                id: 1,
                from: 'Mẹ',
                message: 'Con yêu, mẹ thấy con vui vẻ hơn những ngày gần đây. Mẹ rất vui! 💚',
                date: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
            },
            {
                id: 2,
                from: 'Cha',
                message: 'Cha luôn tự hào về con. Hãy cố gắng và tin vào bản thân nhé!',
                date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString()
            }
        ];
        
        renderReceivedMessages(mockMessages);
        
    } catch (error) {
        BTL.showAlert('Không thể tải dữ liệu', 'error');
    } finally {
        BTL.hideLoading();
    }
}

function renderConnectedParents(parents) {
    const container = document.getElementById('connectedParents');
    
    if (parents.length === 0) {
        container.innerHTML = '<p class="empty-state">Chưa có phụ huynh nào được kết nối</p>';
        return;
    }
    
    container.innerHTML = parents.map(parent => `
        <div class="parent-item">
            <div class="parent-avatar">👤</div>
            <div class="parent-info">
                <strong>${parent.name}</strong>
                <p>${parent.relationship} • ${parent.email}</p>
                <p class="connected-date">Kết nối từ ${BTL.formatDate(parent.connectedDate)}</p>
            </div>
            <button class="btn-remove" onclick="removeParent(${parent.id})" title="Ngắt kết nối">
                ×
            </button>
        </div>
    `).join('');
}

function renderReceivedMessages(messages) {
    const container = document.getElementById('receivedMessages');
    
    if (messages.length === 0) {
        container.innerHTML = '<p class="empty-state">Chưa có tin nhắn nào</p>';
        return;
    }
    
    container.innerHTML = messages.map(msg => `
        <div class="message-item">
            <div class="message-header">
                <strong>${msg.from}</strong>
                <span class="message-date">${BTL.formatDate(msg.date, 'relative')}</span>
            </div>
            <p class="message-content">${msg.message}</p>
        </div>
    `).join('');
}

async function savePrivacySettings() {
    const settings = {
        shareEmotions: document.getElementById('shareEmotions').checked,
        alertParents: document.getElementById('alertParents').checked,
        receiveMessages: document.getElementById('receiveMessages').checked
    };
    
    BTL.showLoading('Đang lưu...');
    
    try {
        await MockAPI.delay(1000);
        BTL.saveToLocalStorage('privacySettings', settings);
        BTL.showAlert('Đã lưu cài đặt!', 'success');
    } catch (error) {
        BTL.showAlert('Không thể lưu cài đặt', 'error');
    } finally {
        BTL.hideLoading();
    }
}

async function sendLetter() {
    const letter = document.getElementById('letterText').value.trim();
    
    if (!letter) {
        BTL.showAlert('Vui lòng viết tâm thư', 'warning');
        return;
    }
    
    BTL.showLoading('Đang gửi...');
    
    try {
        await MockAPI.delay(1500);
        BTL.showAlert('Tâm thư đã được gửi và đang chờ kiểm duyệt', 'success');
        document.getElementById('letterText').value = '';
    } catch (error) {
        BTL.showAlert('Không thể gửi tâm thư', 'error');
    } finally {
        BTL.hideLoading();
    }
}

async function addParent() {
    const email = document.getElementById('parentEmail').value.trim();
    
    if (!email) {
        BTL.showAlert('Vui lòng nhập email', 'warning');
        return;
    }
    
    if (!BTL.validateEmail(email)) {
        BTL.showAlert('Email không hợp lệ', 'error');
        return;
    }
    
    BTL.showLoading('Đang gửi lời mời...');
    
    try {
        await MockAPI.delay(1000);
        BTL.showAlert('Đã gửi lời mời!', 'success');
        BTL.closeModal('addParentModal');
        await loadStudentData();
    } catch (error) {
        BTL.showAlert('Không thể gửi lời mời', 'error');
    } finally {
        BTL.hideLoading();
    }
}

async function removeParent(parentId) {
    if (!confirm('Bạn có chắc muốn ngắt kết nối với phụ huynh này?')) {
        return;
    }
    
    BTL.showLoading('Đang xử lý...');
    
    try {
        await MockAPI.delay(1000);
        BTL.showAlert('Đã ngắt kết nối', 'success');
        await loadStudentData();
    } catch (error) {
        BTL.showAlert('Không thể ngắt kết nối', 'error');
    } finally {
        BTL.hideLoading();
    }
}

function updateDashboard() {
    const timeframe = document.getElementById('timeframeSelect').value;
    loadChildDashboard(selectedChildId);
}

// Load privacy settings on init
const savedSettings = BTL.getFromLocalStorage('privacySettings');
if (savedSettings && document.getElementById('shareEmotions')) {
    document.getElementById('shareEmotions').checked = savedSettings.shareEmotions !== false;
    document.getElementById('alertParents').checked = savedSettings.alertParents !== false;
    document.getElementById('receiveMessages').checked = savedSettings.receiveMessages !== false;
}

console.log('Family page loaded ✓');