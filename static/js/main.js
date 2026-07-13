// Sierra Luxe - Main JavaScript

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Smooth scroll for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var href = this.getAttribute('href');
        // Skip if href is just "#" or empty
        if (href === '#' || href === '') {
            return;
        }
        var target = $(href);
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 70
            }, 1000);
        }
    });
});

// Utility functions
function formatPrice(price) {
    return '$' + parseFloat(price).toFixed(2);
}

function calculateDiscount(originalPrice, discountPrice) {
    if (discountPrice && originalPrice > discountPrice) {
        return Math.round(((originalPrice - discountPrice) / originalPrice) * 100);
    }
    return 0;
}

function showLoadingSpinner() {
    $('body').append('<div class="spinner-overlay"><div class="spinner-border text-light" role="status"><span class="visually-hidden">Loading...</span></div></div>');
}

function hideLoadingSpinner() {
    $('.spinner-overlay').remove();
}

function showMessage(message, type = 'success') {
    const alertClass = type === 'error' ? 'alert-danger' : 
                      type === 'warning' ? 'alert-warning' : 
                      type === 'info' ? 'alert-info' : 'alert-success';
    
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    $('.container').first().prepend(alertHtml);
    
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
}

// AJAX wrapper with error handling
function ajaxRequest(url, method, data, successCallback, errorCallback) {
    showLoadingSpinner();
    
    $.ajax({
        url: url,
        method: method,
        data: data,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function(response) {
            hideLoadingSpinner();
            if (successCallback) {
                successCallback(response);
            }
        },
        error: function(xhr, status, error) {
            hideLoadingSpinner();
            if (errorCallback) {
                errorCallback(xhr, status, error);
            } else {
                showMessage('An error occurred. Please try again.', 'error');
            }
        }
    });
}

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
