document.addEventListener('DOMContentLoaded', function() {
    // Select all reviews checkbox
    const selectAllReviews = document.getElementById('select-all-reviews');
    if (selectAllReviews) {
        selectAllReviews.addEventListener('change', function() {
            const reviewCheckboxes = document.querySelectorAll('.review-checkbox');
            reviewCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
    }
    
    // Update select all checkbox when individual checkboxes change
    const reviewCheckboxes = document.querySelectorAll('.review-checkbox');
    reviewCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const allChecked = Array.from(reviewCheckboxes).every(cb => cb.checked);
            if (selectAllReviews) {
                selectAllReviews.checked = allChecked;
            }
        });
    });
});

// Show delete modal
window.showDeleteModal = function(button) {
    const reviewId = button.getAttribute('data-review-id');
    const customer = button.getAttribute('data-customer');
    
    const modal = new bootstrap.Modal(document.getElementById('deleteReviewModal'));
    const confirmBtn = document.getElementById('deleteReviewModalConfirm');
    const message = document.getElementById('deleteReviewModalMessage');
    
    message.textContent = `Are you sure you want to delete this review by ${customer}? This action cannot be undone.`;
    
    // Remove previous event listeners
    const newConfirmBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
    
    // Add click event to submit the form
    newConfirmBtn.addEventListener('click', function() {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/admin-dashboard/reviews/${reviewId}/delete/`;
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            form.appendChild(csrfToken.cloneNode(true));
        }
        
        document.body.appendChild(form);
        form.submit();
        modal.hide();
    });
    
    modal.show();
};

// Show reject modal
window.showRejectModal = function(button) {
    const reviewId = button.getAttribute('data-review-id');
    const customer = button.getAttribute('data-customer');
    
    const modal = new bootstrap.Modal(document.getElementById('rejectReviewModal'));
    const confirmBtn = document.getElementById('rejectReviewModalConfirm');
    const message = document.getElementById('rejectReviewModalMessage');
    
    message.textContent = `Are you sure you want to reject this review by ${customer}? It will no longer be visible to customers.`;
    
    // Remove previous event listeners
    const newConfirmBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
    
    // Add click event to submit the form
    newConfirmBtn.addEventListener('click', function() {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/admin-dashboard/reviews/${reviewId}/reject/`;
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            form.appendChild(csrfToken.cloneNode(true));
        }
        
        document.body.appendChild(form);
        form.submit();
        modal.hide();
    });
    
    modal.show();
};
