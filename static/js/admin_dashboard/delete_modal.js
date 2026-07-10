// Global Delete Modal Functionality
window.currentDeleteFormId = null;

window.showDeleteModal = function(formId, message) {
    window.currentDeleteFormId = formId;
    
    // Update message if provided
    if (message) {
        const messageElement = document.getElementById('deleteModalMessage');
        if (messageElement) {
            messageElement.textContent = message;
        }
    }
    
    const modalElement = document.getElementById('deleteModal');
    if (!modalElement) {
        console.error('Delete modal element not found');
        return;
    }
    
    // Get existing modal instance or create new one
    let modal = bootstrap.Modal.getInstance(modalElement);
    if (!modal) {
        modal = new bootstrap.Modal(modalElement);
    }
    
    modal.show();
};

// Confirm delete button handler
document.addEventListener('DOMContentLoaded', function() {
    const deleteConfirmBtn = document.getElementById('deleteModalConfirm');
    if (deleteConfirmBtn) {
        deleteConfirmBtn.addEventListener('click', function() {
            if (window.currentDeleteFormId) {
                const form = document.getElementById(window.currentDeleteFormId);
                if (form) {
                    form.submit();
                }
            }
            const modalElement = document.getElementById('deleteModal');
            if (modalElement) {
                const modal = bootstrap.Modal.getInstance(modalElement);
                if (modal) {
                    modal.hide();
                }
            }
        });
    }
});
