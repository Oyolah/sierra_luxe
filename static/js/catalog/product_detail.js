document.addEventListener('DOMContentLoaded', function() {
    // Get data from data attributes
    const productData = document.querySelector('#product-data');
    if (!productData) return;
    
    const videoUrl = productData.dataset.videoUrl || '';
    const imageUrlsString = productData.dataset.imageUrls || '';
    const imageUrls = imageUrlsString ? imageUrlsString.split(',').filter(url => url) : [];
    const sizes = productData.dataset.sizes || '';
    const colors = productData.dataset.colors || '';
    const hasSizes = sizes !== '';
    const hasColors = colors !== '';
    
    // Combine video and images for carousel
    const allMedia = [];
    if (videoUrl) allMedia.push({type: 'video', url: videoUrl});
    imageUrls.forEach(url => allMedia.push({type: 'image', url: url}));

    let currentMediaIndex = 0;

    // Initialize thumbnail navigation buttons
    function updateThumbnailNavButtons() {
        const scrollArea = document.querySelector('#thumbnailScrollArea');
        const upBtn = document.querySelector('#thumbNavUp');
        const downBtn = document.querySelector('#thumbNavDown');
        
        if (!scrollArea) return;
        
        // Disable up button if at top
        if (upBtn) {
            upBtn.disabled = scrollArea.scrollTop <= 0;
        }
        
        // Disable down button if at bottom
        if (downBtn) {
            downBtn.disabled = scrollArea.scrollTop + scrollArea.clientHeight >= scrollArea.scrollHeight - 1;
        }
    }

    // Scroll thumbnails function
    window.scrollThumbnails = function(direction) {
        const scrollArea = document.querySelector('#thumbnailScrollArea');
        if (!scrollArea) return;
        
        const scrollAmount = 88; // 80px thumbnail + 8px gap
        if (direction === 'up') {
            scrollArea.scrollBy({ top: -scrollAmount, behavior: 'smooth' });
        } else {
            scrollArea.scrollBy({ top: scrollAmount, behavior: 'smooth' });
        }
        
        // Update button states after scroll
        setTimeout(updateThumbnailNavButtons, 300);
    };

    // Initialize active thumbnail on page load
    function initializeActiveThumbnail() {
        const mainImage = document.querySelector('#mainImage');
        const mainVideo = document.querySelector('#mainVideo');
        const thumbnails = document.querySelectorAll('.thumbnail');
        
        if (mainVideo && !mainVideo.classList.contains('hidden')) {
            // Video is showing, mark video thumbnail as active
            updateActiveThumbnail(null, true);
        } else if (mainImage && mainImage.src && thumbnails.length > 0) {
            // Image is showing, mark first thumbnail as active
            if (thumbnails.length > 0) {
                thumbnails[0].classList.add('active');
                scrollToThumbnail(thumbnails[0]);
            }
        } else if (thumbnails.length > 0) {
            // No main image, activate first thumbnail
            thumbnails[0].classList.add('active');
            scrollToThumbnail(thumbnails[0]);
        }
        
        // Initialize nav button states
        updateThumbnailNavButtons();
        
        // Add scroll event listener to update button states
        const scrollArea = document.querySelector('#thumbnailScrollArea');
        if (scrollArea) {
            scrollArea.addEventListener('scroll', updateThumbnailNavButtons);
        }
    }

    // Scroll to thumbnail function
    function scrollToThumbnail(thumbnail) {
        const scrollArea = document.querySelector('#thumbnailScrollArea');
        if (!scrollArea || !thumbnail) return;
        
        // Calculate position to center the thumbnail
        const containerHeight = scrollArea.clientHeight;
        const thumbnailTop = thumbnail.offsetTop;
        const thumbnailHeight = thumbnail.offsetHeight;
        const scrollPosition = thumbnailTop - (containerHeight / 2) + (thumbnailHeight / 2);
        
        scrollArea.scrollTo({
            top: scrollPosition,
            behavior: 'smooth'
        });
    }

    // Function to change main media (image or video)
    window.changeImage = function(src, element) {
        const mainImage = document.querySelector('#mainImage');
        const mainVideo = document.querySelector('#mainVideo');
        
        if (mainVideo) {
            mainVideo.style.display = 'none';
            mainVideo.pause();
        }
        if (mainImage) {
            mainImage.style.display = 'block';
            mainImage.src = src;
        }
        
        // Update current index
        currentMediaIndex = allMedia.findIndex(m => m.url === src);
        
        // Update active thumbnail using element reference
        if (element) {
            updateActiveThumbnailByElement(element);
            scrollToThumbnail(element);
        } else {
            updateActiveThumbnail(src);
        }
    }

    // Function to show video
    window.showVideo = function() {
        const mainImage = document.querySelector('#mainImage');
        const mainVideo = document.querySelector('#mainVideo');
        
        if (mainImage) {
            mainImage.style.display = 'none';
        }
        if (mainVideo) {
            mainVideo.style.display = 'block';
            mainVideo.play();
        }
        
        // Update current index
        currentMediaIndex = allMedia.findIndex(m => m.type === 'video');
        
        // Update active thumbnail for video
        updateActiveThumbnail(null, true);
        
        // Scroll to video thumbnail
        const videoThumbnail = document.querySelector('.video-thumbnail');
        if (videoThumbnail) {
            scrollToThumbnail(videoThumbnail);
        }
    }

    // Function to update active thumbnail styling by element reference
    function updateActiveThumbnailByElement(element) {
        // Remove active class from all thumbnails
        document.querySelectorAll('.thumbnail').forEach(thumb => {
            thumb.classList.remove('active');
        });
        
        // Remove active class from video thumbnail
        const videoThumbnail = document.querySelector('.video-thumbnail');
        if (videoThumbnail) {
            videoThumbnail.classList.remove('active');
        }
        
        // Add active class to the clicked element
        if (element) {
            element.classList.add('active');
        }
    }

    // Function to update active thumbnail styling
    function updateActiveThumbnail(src, isVideo = false) {
        // Remove active class from all thumbnails
        document.querySelectorAll('.thumbnail').forEach(thumb => {
            thumb.classList.remove('active');
        });
        
        // Remove active class from video thumbnail
        const videoThumbnail = document.querySelector('.video-thumbnail');
        if (videoThumbnail) {
            videoThumbnail.classList.remove('active');
        }
        
        // Add active class to selected thumbnail
        if (isVideo && videoThumbnail) {
            videoThumbnail.classList.add('active');
        } else if (src) {
            // Find thumbnail with matching src (handle URL variations)
            const thumbnails = document.querySelectorAll('.thumbnail');
            thumbnails.forEach(thumb => {
                // Compare URLs, handling potential encoding differences
                if (thumb.src === src || thumb.src === decodeURIComponent(src) || encodeURIComponent(thumb.src) === encodeURIComponent(src)) {
                    thumb.classList.add('active');
                    scrollToThumbnail(thumb);
                }
            });
        }
    }

    // Navigate carousel using centralized utility
    window.navigateCarousel = function(direction) {
        if (allMedia.length === 0) return;
        
        // Check if CarouselUtils is available
        if (typeof CarouselUtils !== 'undefined') {
            currentMediaIndex = CarouselUtils.navigate(
                allMedia, 
                currentMediaIndex, 
                direction, 
                (media, index) => {
                    currentMediaIndex = index;
                    if (media.type === 'video') {
                        showVideo();
                    } else {
                        changeImage(media.url);
                    }
                }
            );
        } else {
            // Fallback carousel navigation
            currentMediaIndex = currentMediaIndex + direction;
            if (currentMediaIndex < 0) {
                currentMediaIndex = allMedia.length - 1;
            } else if (currentMediaIndex >= allMedia.length) {
                currentMediaIndex = 0;
            }
            
            const media = allMedia[currentMediaIndex];
            if (media.type === 'video') {
                showVideo();
            } else {
                changeImage(media.url);
            }
        }
    };

    // Populate size options using centralized utility
    const sizeContainer = document.querySelector('#size-options');
    if (sizeContainer && sizes && typeof FormUtils !== 'undefined') {
        FormUtils.createOptionButtons(
            sizes,
            sizeContainer,
            'size-btn',
            function() { selectSize(this); }
        );
    }

    // Populate color options using centralized utility
    const colorContainer = document.querySelector('#color-options');
    if (colorContainer && colors && typeof FormUtils !== 'undefined') {
        FormUtils.createColorOptions(
            colors,
            colorContainer,
            function() { selectColor(this); }
        );
    }

    // Initialize active thumbnail on page load
    initializeActiveThumbnail();
});

function selectSize(btn) {
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    // Update hidden form field
    document.querySelector('#cart-size').value = btn.textContent.trim();
}

function selectColor(div) {
    document.querySelectorAll('.color-option').forEach(c => c.classList.remove('active'));
    div.classList.add('active');
    // Update hidden form field
    document.querySelector('#cart-color').value = div.dataset.color || div.title;
}

function changeQuantity(delta) {
    const input = document.querySelector('#quantity');
    const newValue = parseInt(input.value) + delta;
    const max = parseInt(input.max);
    
    if (newValue >= 1 && newValue <= max) {
        input.value = newValue;
    }
    // Update hidden form field
    document.querySelector('#cart-quantity').value = input.value;
}

// Handle add to cart form submission
const addToCartForm = document.querySelector('#add-to-cart-form');
if (addToCartForm) {
    addToCartForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get data from data attributes
        const productData = document.querySelector('#product-data');
        const hasSizes = productData.dataset.sizes !== '';
        const hasColors = productData.dataset.colors !== '';
        
        // Update quantity before submit
        const quantity = document.querySelector('#quantity');
        if (quantity) {
            document.querySelector('#cart-quantity').value = quantity.value;
        }
        
        // Validate size selection if product has sizes
        if (hasSizes) {
            const selectedSize = document.querySelector('.size-btn.active');
            if (!selectedSize) {
                showModal('validationModal', 'Selection Required', 'Please select a size before adding to cart.');
                return false;
            }
            document.querySelector('#cart-size').value = selectedSize.textContent.trim();
        }
        
        // Validate color selection if product has colors
        if (hasColors) {
            const selectedColor = document.querySelector('.color-option.active');
            if (!selectedColor) {
                showModal('validationModal', 'Selection Required', 'Please select a color before adding to cart.');
                return false;
            }
            document.querySelector('#cart-color').value = selectedColor.dataset.color || selectedColor.title;
        }
        
        // Submit via AJAX
        const formData = new FormData(this);
        const csrftoken = this.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch(this.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Add to cart response:', data);
            if (data.success) {
                // Show success message
                showSuccessMessage(data.message);
                
                // Update cart count in navbar
                updateCartCount(data.cart_count);
            } else {
                alert(data.message || 'Error adding to cart. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error adding to cart:', error);
            alert('Error adding to cart. Please try again.');
        });
    });
}

// Show success message
function showSuccessMessage(message) {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = 'alert alert-success position-fixed';
    toast.style.cssText = 'top: 80px; right: 20px; z-index: 9999; min-width: 300px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);';
    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-check-circle me-2"></i>
            <div class="flex-grow-1">${message}</div>
            <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Update cart count in navbar
function updateCartCount(count) {
    let cartBadge = document.querySelector('.cart-count');
    const cartDropdown = document.querySelector('#cartDropdown');
    
    if (!cartBadge && cartDropdown && count > 0) {
        // Create badge if it doesn't exist
        cartBadge = document.createElement('span');
        cartBadge.className = 'position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger cart-count';
        cartDropdown.appendChild(cartBadge);
    }
    
    if (cartBadge) {
        cartBadge.textContent = count;
        if (count === 0) {
            cartBadge.classList.add('d-none');
        } else {
            cartBadge.classList.remove('d-none');
        }
    }
    
    // Reload cart dropdown preview if function exists
    if (typeof loadCartPreview === 'function') {
        loadCartPreview();
    }
}
