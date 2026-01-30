// SyncClipboard Mobile Web App

// Configuration
let config = {
    serverUrl: '',
    username: '',
    password: '',
    autoSync: false,
    syncInterval: 5000 // 5 seconds
};

let autoSyncTimer = null;

// Load configuration from localStorage
function loadConfig() {
    const savedConfig = localStorage.getItem('syncclipboard_config');
    if (savedConfig) {
        config = JSON.parse(savedConfig);
        document.getElementById('serverUrl').value = config.serverUrl || '';
        document.getElementById('username').value = config.username || '';
        document.getElementById('password').value = config.password || '';
        document.getElementById('autoSync').checked = config.autoSync || false;
        
        if (config.autoSync) {
            startAutoSync();
        }
    }
}

// Save configuration to localStorage
function saveSettings() {
    config.serverUrl = document.getElementById('serverUrl').value.trim();
    config.username = document.getElementById('username').value.trim();
    config.password = document.getElementById('password').value.trim();
    
    if (!config.serverUrl || !config.username || !config.password) {
        showStatus('Please fill in all settings', 'error');
        return;
    }
    
    // Remove trailing slash from URL
    config.serverUrl = config.serverUrl.replace(/\/$/, '');
    
    localStorage.setItem('syncclipboard_config', JSON.stringify(config));
    showStatus('✓ Settings saved successfully', 'success');
}

// Show status message
function showStatus(message, type = 'success') {
    const statusEl = document.getElementById('statusMessage');
    statusEl.textContent = message;
    statusEl.className = 'status ' + type;
    statusEl.classList.remove('hidden');
    
    setTimeout(() => {
        statusEl.classList.add('hidden');
    }, 3000);
}

// Show clipboard preview
function showClipboardPreview(text) {
    const previewEl = document.getElementById('clipboardPreview');
    previewEl.textContent = text || '(empty)';
    previewEl.classList.remove('hidden');
}

// Get auth header
function getAuthHeader() {
    return 'Basic ' + btoa(config.username + ':' + config.password);
}

// Upload clipboard to server
async function uploadClipboard() {
    if (!config.serverUrl || !config.username || !config.password) {
        showStatus('Please configure settings first', 'error');
        return;
    }
    
    try {
        // Get clipboard content
        const text = await navigator.clipboard.readText();
        
        if (!text) {
            showStatus('Clipboard is empty', 'error');
            return;
        }
        
        showClipboardPreview(text);
        
        // Prepare clipboard data
        const clipboardData = {
            Type: 'Text',
            Clipboard: text,
            File: ''
        };
        
        // Upload to server
        const response = await fetch(`${config.serverUrl}/SyncClipboard.json`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': getAuthHeader()
            },
            body: JSON.stringify(clipboardData)
        });
        
        if (response.ok) {
            showStatus('✓ Clipboard uploaded successfully', 'success');
        } else if (response.status === 401) {
            showStatus('✗ Authentication failed', 'error');
        } else {
            showStatus('✗ Upload failed: ' + response.statusText, 'error');
        }
    } catch (error) {
        showStatus('✗ Error: ' + error.message, 'error');
    }
}

// Download clipboard from server
async function downloadClipboard() {
    if (!config.serverUrl || !config.username || !config.password) {
        showStatus('Please configure settings first', 'error');
        return;
    }
    
    try {
        // Download from server
        const response = await fetch(`${config.serverUrl}/SyncClipboard.json`, {
            method: 'GET',
            headers: {
                'Authorization': getAuthHeader()
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                showStatus('✗ Authentication failed', 'error');
            } else {
                showStatus('✗ Download failed: ' + response.statusText, 'error');
            }
            return;
        }
        
        const clipboardData = await response.json();
        const clipboardType = clipboardData.Type || 'Text';
        
        if (clipboardType === 'Text') {
            const text = clipboardData.Clipboard || '';
            
            // Set to clipboard
            await navigator.clipboard.writeText(text);
            
            showClipboardPreview(text);
            showStatus('✓ Clipboard downloaded successfully', 'success');
        } else if (clipboardType === 'Image') {
            showStatus('✓ Image clipboard detected (preview not available on mobile)', 'success');
        } else {
            showStatus('✓ Downloaded: ' + clipboardType, 'success');
        }
    } catch (error) {
        showStatus('✗ Error: ' + error.message, 'error');
    }
}

// Toggle auto sync
function toggleAutoSync() {
    config.autoSync = document.getElementById('autoSync').checked;
    localStorage.setItem('syncclipboard_config', JSON.stringify(config));
    
    if (config.autoSync) {
        startAutoSync();
        showStatus('✓ Auto-sync enabled', 'success');
    } else {
        stopAutoSync();
        showStatus('✓ Auto-sync disabled', 'success');
    }
}

// Start auto sync
function startAutoSync() {
    if (autoSyncTimer) {
        clearInterval(autoSyncTimer);
    }
    
    autoSyncTimer = setInterval(() => {
        downloadClipboard();
    }, config.syncInterval);
}

// Stop auto sync
function stopAutoSync() {
    if (autoSyncTimer) {
        clearInterval(autoSyncTimer);
        autoSyncTimer = null;
    }
}

// Check clipboard API support
function checkClipboardSupport() {
    if (!navigator.clipboard) {
        showStatus('⚠️ Clipboard API not supported. Please use HTTPS.', 'error');
        document.getElementById('uploadBtn').disabled = true;
        document.getElementById('downloadBtn').disabled = true;
        return false;
    }
    return true;
}

// Initialize app
function init() {
    loadConfig();
    checkClipboardSupport();
    
    // Request notification permission for background sync
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
}

// Register service worker for PWA
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('service-worker.js')
        .then(reg => console.log('Service Worker registered'))
        .catch(err => console.log('Service Worker registration failed:', err));
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
