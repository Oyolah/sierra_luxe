document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('#searchInput');
    const clearSearch = document.querySelector('#clearSearch');
    const searchForm = document.querySelector('#searchForm');
    
    // Show/hide clear button based on initial value
    if (searchInput.value) {
        clearSearch.style.display = 'block';
    }
    
    // Show/hide clear button based on input
    searchInput.addEventListener('input', function() {
        clearSearch.style.display = this.value ? 'block' : 'none';
    });
    
    // Clear search
    clearSearch.addEventListener('click', function() {
        searchInput.value = '';
        clearSearch.style.display = 'none';
        
        // If on products page, clear everything like Clear Filters does
        if (window.location.pathname === '/products/' || window.location.pathname.startsWith('/products')) {
            // Clear URL completely (removes all parameters including search and filters)
            window.history.pushState({}, '', window.location.pathname);
            
            // Trigger fetch to reload all products
            if (typeof window.fetchProducts === 'function') {
                window.fetchProducts();
            } else {
                // Fallback: reload page without any parameters
                window.location.href = window.location.pathname;
            }
        } else {
            searchForm.submit();
        }
    });
    
    // Handle search form submission with AJAX if on products page
    searchForm.addEventListener('submit', function(e) {
        if (window.location.pathname === '/products/') {
            e.preventDefault();
            performSearch(searchInput.value);
        }
    });
    
    // Cart dropdown hover functionality
    const cartDropdown = document.querySelector('#cart-dropdown');
    const cartDropdownMenu = document.querySelector('#cart-dropdown-menu');
    let cartHoverTimeout;
    
    if (cartDropdown && cartDropdownMenu) {
        cartDropdown.addEventListener('mouseenter', function() {
            clearTimeout(cartHoverTimeout);
            cartDropdownMenu.style.display = 'block';
            loadCartPreview();
        });
        
        cartDropdown.addEventListener('mouseleave', function() {
            cartHoverTimeout = setTimeout(() => {
                cartDropdownMenu.style.display = 'none';
            }, 300);
        });
        
        cartDropdownMenu.addEventListener('mouseenter', function() {
            clearTimeout(cartHoverTimeout);
        });
        
        cartDropdownMenu.addEventListener('mouseleave', function() {
            cartDropdownMenu.style.display = 'none';
        });
    }
    
    window.loadCartPreview = function() {
        fetch('/cart/preview/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const cartItemsPreview = document.querySelector('#cart-items-preview');
                const cartDropdownTotal = document.querySelector('#cart-dropdown-total');
                
                if (!cartItemsPreview || !cartDropdownTotal) {
                    console.error('Cart preview elements not found');
                    return;
                }
                
                if (data.success) {
                    if (data.items.length === 0) {
                        cartItemsPreview.innerHTML = '<div class="text-center py-4 text-muted">Your cart is empty</div>';
                        cartDropdownTotal.textContent = '€0.00';
                    } else {
                        let itemsHTML = '';
                        data.items.forEach(item => {
                            itemsHTML += `
                                <div class="d-flex gap-2 p-3 border-bottom">
                                    <img src="${item.product_image}" alt="${item.product_name}" 
                                         style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;">
                                    <div class="flex-grow-1">
                                        <h6 class="mb-0 small">${item.product_name}</h6>
                                        <p class="text-muted small mb-0">Qty: ${item.quantity}</p>
                                        ${item.size ? `<p class="text-muted small mb-0">Size: ${item.size}</p>` : ''}
                                    </div>
                                    <div class="text-end">
                                        <p class="mb-0 fw-bold small">${data.currency_symbol}${item.subtotal.toFixed(2)}</p>
                                    </div>
                                </div>
                            `;
                        });
                        cartItemsPreview.innerHTML = itemsHTML;
                        cartDropdownTotal.textContent = `${data.currency_symbol}${data.cart_total.toFixed(2)}`;
                    }
                } else {
                    cartItemsPreview.innerHTML = '<div class="text-center py-4 text-danger">Error loading cart</div>';
                    console.error('Cart preview error:', data.error);
                }
            })
            .catch(error => {
                console.error('Error loading cart preview:', error);
                const cartItemsPreview = document.querySelector('#cart-items-preview');
                if (cartItemsPreview) {
                    cartItemsPreview.innerHTML = '<div class="text-center py-4 text-danger">Failed to load cart</div>';
                }
            });
    }
    
    // Function to perform AJAX search using centralized utilities
    function performSearch(searchTerm) {
        const params = UrlUtils.getParams();
        
        // Remove search param if empty, otherwise set it
        if (searchTerm && searchTerm.trim()) {
            params.search = searchTerm;
        } else {
            delete params.search;
        }
        
        UrlUtils.updateUrl(params);
        
        // Trigger the products page AJAX filter
        if (typeof window.fetchProducts === 'function') {
            window.fetchProducts();
        } else {
            // Fallback: reload page
            const queryString = UrlUtils.buildQueryString(params);
            window.location.href = window.location.pathname + (queryString ? '?' + queryString : '');
        }
    }
});
