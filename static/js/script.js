// ========================================
// SentimentIQ Frontend JavaScript
// ========================================

const API_BASE = 'http://localhost:8000';
let authToken = null;
let currentUser = null;

// ===== Initialization =====
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});

// ===== Authentication =====
function showAuthModal(type) {
    if (authToken) {
        switchTab('analyze');
        return;
    }
    switchAuthForm(type);
    document.getElementById('auth-section').scrollIntoView({ behavior: 'smooth' });
}

function switchAuthForm(type) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (type === 'login') {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
    } else {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
    }
}

async function handleLogin(e) {
    e.preventDefault();
    showSpinner(true);

    try {
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }

        const data = await response.json();
        authToken = data.access_token;
        currentUser = data.user;
        
        localStorage.setItem('token', authToken);
        localStorage.setItem('user', JSON.stringify(currentUser));

        showToast('Logged in successfully!', 'success');
        showDashboard();
        showSpinner(false);
    } catch (error) {
        showToast(error.message, 'error');
        showSpinner(false);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    showSpinner(true);

    try {
        const username = document.getElementById('registerUsername').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;

        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Registration failed');
        }

        const data = await response.json();
        authToken = data.access_token;
        currentUser = data.user;
        
        localStorage.setItem('token', authToken);
        localStorage.setItem('user', JSON.stringify(currentUser));

        showToast('Account created successfully!', 'success');
        showDashboard();
        showSpinner(false);
    } catch (error) {
        showToast(error.message, 'error');
        showSpinner(false);
    }
}

function checkAuth() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');

    if (token && user) {
        authToken = token;
        currentUser = JSON.parse(user);
        showDashboard();
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    document.getElementById('dashboard').classList.add('hidden');
    document.getElementById('auth-section').classList.remove('hidden');
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('registerForm').classList.add('hidden');
    showToast('Logged out successfully', 'success');
}

// ===== Dashboard =====
function showDashboard() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('dashboard').classList.remove('hidden');
    switchTab('analyze');
    loadStats();
}

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.add('hidden');
    });

    // Remove active state from buttons
    document.querySelectorAll('.nav-item').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName + 'Tab').classList.remove('hidden');

    // Add active state to button
    event.target.classList.add('active');

    // Load tab-specific data
    if (tabName === 'history') {
        loadHistory();
    } else if (tabName === 'stats') {
        loadStats();
    }
}

// ===== Analysis Functions =====
async function analyzeText() {
    const text = document.getElementById('textInput').value;

    if (!text.trim()) {
        showToast('Please enter text to analyze', 'error');
        return;
    }

    showSpinner(true);

    try {
        const response = await fetch(`${API_BASE}/analyze/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }

        const result = await response.json();
        displayResults(result);
        showToast('Analysis complete!', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        showSpinner(false);
    }
}

async function analyzeURL() {
    const url = document.getElementById('urlInput').value;

    if (!url.trim()) {
        showToast('Please enter a URL', 'error');
        return;
    }

    showSpinner(true);

    try {
        const response = await fetch(`${API_BASE}/analyze/url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ url })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'URL analysis failed');
        }

        const result = await response.json();
        displayResults(result);
        showToast('URL analyzed successfully!', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        showSpinner(false);
    }
}

async function analyzeCSV() {
    const file = document.getElementById('csvFile').files[0];
    const columnName = document.getElementById('columnName').value || null;

    if (!file) {
        showToast('Please select a CSV file', 'error');
        return;
    }

    showSpinner(true);

    try {
        const formData = new FormData();
        formData.append('file', file);
        if (columnName) {
            formData.append('text_column', columnName);
        }

        const response = await fetch(`${API_BASE}/analyze/csv`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            },
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'CSV analysis failed');
        }

        const result = await response.json();
        displayBatchResults(result);
        showToast('CSV analysis complete!', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        showSpinner(false);
    }
}

function displayResults(result) {
    // Hide batch results, show single results
    document.getElementById('batchResultsSection').classList.add('hidden');
    document.getElementById('resultsSection').classList.remove('hidden');

    // Update sentiment badge
    const sentimentLabel = document.getElementById('sentimentLabel');
    sentimentLabel.textContent = result.sentiment_label.toUpperCase();
    sentimentLabel.className = `sentiment-badge ${result.sentiment_label}`;

    // Update confidence
    document.getElementById('confidenceScore').textContent = `Confidence: ${(result.confidence * 100).toFixed(1)}%`;

    // Update polarity bar
    const polarity = result.polarity;
    const polarityPercent = ((polarity + 1) / 2) * 100;
    document.getElementById('polarityBar').style.width = polarityPercent + '%';
    document.getElementById('polarityValue').textContent = polarity.toFixed(2);

    // Update subjectivity bar
    const subjectivity = result.subjectivity;
    const subjectivityPercent = subjectivity * 100;
    document.getElementById('subjectivityBar').style.width = subjectivityPercent + '%';
    document.getElementById('subjectivityValue').textContent = subjectivity.toFixed(2);

    // Update VADER scores
    document.getElementById('vaderCompound').textContent = result.vader_compound.toFixed(2);
    document.getElementById('vaderPositive').textContent = result.vader_positive.toFixed(2);
    document.getElementById('vaderNegative').textContent = result.vader_negative.toFixed(2);
    document.getElementById('vaderNeutral').textContent = result.vader_neutral.toFixed(2);

    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

function displayBatchResults(result) {
    // Hide single results, show batch results
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('batchResultsSection').classList.remove('hidden');

    document.getElementById('batchTotal').textContent = result.total_rows;
    document.getElementById('batchPositive').textContent = result.positive_count;
    document.getElementById('batchNegative').textContent = result.negative_count;
    document.getElementById('batchNeutral').textContent = result.neutral_count;

    document.getElementById('batchResultsSection').scrollIntoView({ behavior: 'smooth' });
}

function handleFileSelect() {
    const file = document.getElementById('csvFile').files[0];
    if (file) {
        showToast(`File selected: ${file.name}`, 'info');
    }
}

// ===== History =====
async function loadHistory() {
    showSpinner(true);

    try {
        const response = await fetch(`${API_BASE}/analysis/history?limit=20`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to load history');
        }

        const analyses = await response.json();
        displayHistory(analyses);
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        showSpinner(false);
    }
}

function displayHistory(analyses) {
    const historyList = document.getElementById('historyList');

    if (analyses.length === 0) {
        historyList.innerHTML = '<p class="empty-state"><i class="fas fa-inbox"></i> No analyses yet</p>';
        return;
    }

    historyList.innerHTML = analyses.map(analysis => `
        <div class="history-item">
            <div class="history-text">
                <p><strong>${analysis.input_type.toUpperCase()}</strong></p>
                <p style="color: #999; font-size: 13px;">
                    ${analysis.input_text.substring(0, 100)}${analysis.input_text.length > 100 ? '...' : ''}
                </p>
                <p style="color: #999; font-size: 12px;">
                    ${new Date(analysis.created_at).toLocaleString()}
                </p>
            </div>
            <span class="history-sentiment ${analysis.sentiment_label}">
                ${analysis.sentiment_label.toUpperCase()}
            </span>
        </div>
    `).join('');
}

// ===== Statistics =====
async function loadStats() {
    showSpinner(true);

    try {
        const response = await fetch(`${API_BASE}/analysis/stats/summary`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to load statistics');
        }

        const stats = await response.json();
        displayStats(stats);
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        showSpinner(false);
    }
}

function displayStats(stats) {
    document.getElementById('statTotal').textContent = stats.total_analyses;
    document.getElementById('statPositive').textContent = stats.positive_count;
    document.getElementById('statNegative').textContent = stats.negative_count;
    document.getElementById('statNeutral').textContent = stats.neutral_count;
    document.getElementById('statAvgConfidence').textContent = (stats.average_confidence * 100).toFixed(1) + '%';
    document.getElementById('statAvgPolarity').textContent = stats.average_polarity.toFixed(2);
}

// ===== UI Helpers =====
function showSpinner(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (show) {
        spinner.classList.remove('hidden');
    } else {
        spinner.classList.add('hidden');
    }
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    let icon = 'fas fa-info-circle';
    if (type === 'success') icon = 'fas fa-check-circle';
    if (type === 'error') icon = 'fas fa-exclamation-circle';

    toast.innerHTML = `
        <i class="${icon}"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ===== Error Handling =====
window.addEventListener('error', (e) => {
    console.error('Error:', e.error);
    showToast('An unexpected error occurred', 'error');
});
