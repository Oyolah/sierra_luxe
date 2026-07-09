/**
 * Session Timeout Manager
 * Automatically logs out users after 30 minutes of inactivity
 * Shows warning dialog 1 minute before session expires
 */

class SessionTimeoutManager {
    constructor(options = {}) {
        this.timeout = options.timeout || 30 * 60 * 1000; // 30 minutes in milliseconds
        this.warningTime = options.warningTime || 1 * 60 * 1000; // 1 minute in milliseconds
        this.warningShown = false;
        this.timer = null;
        this.warningTimer = null;
        this.lastActivity = Date.now();
        this.checkInterval = 30 * 1000; // Check every 30 seconds
        
        this.init();
    }
    
    init() {
        // Only initialize if user is authenticated
        if (this.isUserAuthenticated()) {
            this.startActivityTracking();
            this.startSessionTimer();
            this.startInactivityCheck();
        }
    }
    
    isUserAuthenticated() {
        // Check if user is authenticated by looking for user data
        return document.body.classList.contains('user-authenticated') || 
               document.querySelector('[data-user-authenticated="true"]') !== null;
    }
    
    startActivityTracking() {
        // Track user activity to reset timer
        const events = [
            'mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'
        ];
        
        events.forEach(event => {
            document.addEventListener(event, () => this.resetTimer(), true);
        });
        
        // Also track visibility changes
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.resetTimer();
            }
        });
    }
    
    resetTimer() {
        this.lastActivity = Date.now();
        this.warningShown = false;
        
        // Clear existing timers
        if (this.timer) clearTimeout(this.timer);
        if (this.warningTimer) clearTimeout(this.warningTimer);
        
        // Restart timers
        this.startSessionTimer();
        this.startWarningTimer();
    }
    
    startSessionTimer() {
        this.timer = setTimeout(() => {
            this.logout();
        }, this.timeout);
    }
    
    startWarningTimer() {
        this.warningTimer = setTimeout(() => {
            this.showWarning();
        }, this.timeout - this.warningTime);
    }
    
    startInactivityCheck() {
        // Periodically check if user has been inactive
        setInterval(() => {
            const inactiveTime = Date.now() - this.lastActivity;
            
            if (inactiveTime >= this.timeout) {
                this.logout();
            }
        }, this.checkInterval);
    }
    
    showWarning() {
        if (this.warningShown) return;
        this.warningShown = true;
        
        const warningModal = document.getElementById('session-timeout-warning');
        if (warningModal) {
            warningModal.classList.add('show');
            warningModal.style.display = 'block';
            
            // Start countdown
            this.startCountdown();
        }
    }
    
    startCountdown() {
        let timeLeft = 60; // 60 seconds
        const countdownElement = document.getElementById('session-countdown');
        
        if (countdownElement) {
            const countdownInterval = setInterval(() => {
                timeLeft--;
                countdownElement.textContent = timeLeft;
                
                if (timeLeft <= 0) {
                    clearInterval(countdownInterval);
                    this.logout();
                }
            }, 1000);
        }
    }
    
    extendSession() {
        // User clicked "Stay Signed In"
        this.hideWarning();
        this.resetTimer();
    }
    
    hideWarning() {
        const warningModal = document.getElementById('session-timeout-warning');
        if (warningModal) {
            warningModal.classList.remove('show');
            warningModal.style.display = 'none';
        }
    }
    
    logout() {
        // Clear all timers
        if (this.timer) clearTimeout(this.timer);
        if (this.warningTimer) clearTimeout(this.warningTimer);
        
        // Set flag to show inactivity message
        sessionStorage.setItem('session_timeout', 'true');
        
        // Redirect to logout with session timeout flag
        window.location.href = '/logout/?session_timeout=true';
    }
}

// Initialize session timeout manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.sessionTimeoutManager = new SessionTimeoutManager({
        timeout: 30 * 60 * 1000, // 30 minutes
        warningTime: 1 * 60 * 1000 // 1 minute
    });
});

// Extend session when user clicks "Stay Signed In"
document.addEventListener('click', (e) => {
    if (e.target && e.target.id === 'extend-session-btn') {
        e.preventDefault();
        if (window.sessionTimeoutManager) {
            window.sessionTimeoutManager.extendSession();
        }
    }
});
