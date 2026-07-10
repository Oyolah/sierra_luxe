// Initialize modal functionality
document.addEventListener('DOMContentLoaded', function() {
    const modals = document.querySelectorAll('[data-modal-id]');
    
    modals.forEach(function(modal) {
        const modalId = modal.getAttribute('data-modal-id');
        
        // Store callback function
        window[modalId + '_callback'] = null;
        
        // Confirm button click handler
        const confirmBtn = document.querySelector(`[data-modal-confirm="${modalId}"]`);
        if (confirmBtn) {
            confirmBtn.addEventListener('click', function() {
                const callback = window[modalId + '_callback'];
                if (callback && typeof callback === 'function') {
                    callback();
                }
                // Close modal
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) {
                    bsModal.hide();
                }
            });
        }
    });
});

// Global function to show modal
window.showModal = function(modalId, title, body, onConfirm) {
    const modal = document.querySelector('#' + modalId);
    if (!modal) {
        console.error('Modal not found:', modalId);
        return;
    }
    
    // Update title if provided
    if (title) {
        const titleElement = document.querySelector('#' + modalId + 'Label');
        if (titleElement) {
            titleElement.textContent = title;
        }
    }
    
    // Update body if provided
    if (body) {
        const bodyElement = document.querySelector('#' + modalId + 'Body');
        if (bodyElement) {
            bodyElement.innerHTML = body;
        }
    }
    
    // Store callback
    if (onConfirm) {
        window[modalId + '_callback'] = onConfirm;
    }
    
    // Show modal
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
};

// Global function to hide modal
window.hideModal = function(modalId) {
    const modal = document.querySelector('#' + modalId);
    if (modal) {
        const bsModal = bootstrap.Modal.getInstance(modal);
        if (bsModal) {
            bsModal.hide();
        }
    }
};
