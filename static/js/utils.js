/**
 * Sierra Luxe - JavaScript Utilities
 * Centralized utility functions to avoid code repetition
 */

// AJAX Utility - Similar to React's useFetch hook
const AjaxUtils = {
    /**
     * Generic AJAX fetch function
     * @param {string} url - The URL to fetch
     * @param {Object} options - Fetch options
     * @returns {Promise} - Promise with response data
     */
    async fetch(url, options = {}) {
        const defaultOptions = {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, defaultOptions);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('AJAX request failed:', error);
            throw error;
        }
    },

    /**
     * Fetch with loading state
     * @param {string} url - The URL to fetch
     * @param {HTMLElement} loadingElement - Element to show/hide loading state
     * @param {Function} onSuccess - Callback on success
     * @param {Function} onError - Callback on error
     */
    async fetchWithLoading(url, loadingElement, onSuccess, onError) {
        if (loadingElement) {
            loadingElement.classList.add('active');
        }

        try {
            const data = await this.fetch(url);
            if (onSuccess) onSuccess(data);
        } catch (error) {
            if (onError) onError(error);
        } finally {
            if (loadingElement) {
                loadingElement.classList.remove('active');
            }
        }
    }
};

// URL Utilities
const UrlUtils = {
    /**
     * Get URL parameters as object
     * @returns {Object} - URL parameters
     */
    getParams() {
        const params = new URLSearchParams(window.location.search);
        const result = {};
        for (const [key, value] of params) {
            result[key] = value;
        }
        return result;
    },

    /**
     * Update URL without reload
     * @param {Object} params - Parameters to update
     */
    updateUrl(params) {
        const url = new URL(window.location);
        Object.keys(params).forEach(key => {
            if (params[key]) {
                url.searchParams.set(key, params[key]);
            } else {
                url.searchParams.delete(key);
            }
        });
        window.history.pushState({}, '', url);
    },

    /**
     * Build query string from object
     * @param {Object} params - Parameters object
     * @returns {string} - Query string
     */
    buildQueryString(params) {
        return new URLSearchParams(params).toString();
    }
};

// DOM Utilities
const DomUtils = {
    /**
     * Update element content safely
     * @param {HTMLElement} element - Element to update
     * @param {string} content - New content
     */
    setContent(element, content) {
        if (element) {
            element.innerHTML = content;
        }
    }
};

// Product Rendering Utilities
const ProductUtils = {
    /**
     * Generate product card HTML
     * @param {Object} product - Product object
     * @param {string} currencySymbol - Currency symbol
     * @param {string} placeholderImage - Placeholder image URL
     * @returns {string} - Product card HTML
     */
    renderProductCard(product, currencySymbol = 'Le', placeholderImage = '/static/images/placeholder.jpg') {
        const imageUrl = product.image || placeholderImage;
        const discountHtml = product.discount_price ? 
            `<p class="text-muted small mb-0"><s>${currencySymbol}${product.discount_price}</s></p>` : '';
        
        return `
            <div class="col-md-4">
                <a href="/product/${product.slug}/" class="text-decoration-none">
                    <div class="card product-card h-100">
                        <img src="${imageUrl}" alt="${product.name}" class="product-image">
                        <div class="card-body">
                            <h6 class="card-title text-dark">${product.name}</h6>
                            <p class="card-text text-muted small">${product.description}</p>
                            <p class="price mb-0">${currencySymbol}${product.price}</p>
                            ${discountHtml}
                        </div>
                    </div>
                </a>
            </div>
        `;
    },

    /**
     * Render multiple product cards
     * @param {Array} products - Array of product objects
     * @param {string} currencySymbol - Currency symbol
     * @param {string} placeholderImage - Placeholder image URL
     * @returns {string} - Product cards HTML
     */
    renderProductCards(products, currencySymbol = 'Le', placeholderImage = '/static/images/placeholder.jpg') {
        if (products.length === 0) {
            return '<div class="col-12 text-center"><p class="text-muted">No products found matching your criteria.</p></div>';
        }
        
        return products.map(product => 
            this.renderProductCard(product, currencySymbol, placeholderImage)
        ).join('');
    }
};

// Form Utilities
const FormUtils = {
    /**
     * Create option buttons from comma-separated string
     * @param {string} optionsString - Comma-separated options
     * @param {HTMLElement} container - Container element
     * @param {string} buttonClass - CSS class for buttons
     * @param {Function} onClick - Click handler
     */
    createOptionButtons(optionsString, container, buttonClass, onClick) {
        if (!optionsString || !container) return;
        
        const options = optionsString.split(',').map(s => s.trim());
        options.forEach(option => {
            const btn = document.createElement('button');
            btn.className = buttonClass;
            btn.textContent = option;
            btn.onclick = onClick;
            container.appendChild(btn);
        });
    },

    /**
     * Create color option divs from comma-separated string
     * @param {string} colorsString - Comma-separated colors
     * @param {HTMLElement} container - Container element
     * @param {Function} onClick - Click handler
     */
    createColorOptions(colorsString, container, onClick) {
        if (!colorsString || !container) return;
        
        const colors = colorsString.split(',').map(c => c.trim());
        colors.forEach(color => {
            const div = document.createElement('div');
            div.className = 'color-option';
            div.style.backgroundColor = color;
            div.title = color;
            div.onclick = onClick;
            container.appendChild(div);
        });
    }
};

// Carousel Utilities
const CarouselUtils = {
    /**
     * Navigate carousel with wraparound
     * @param {Array} items - Array of items
     * @param {number} currentIndex - Current index
     * @param {number} direction - Direction (-1 or 1)
     * @param {Function} onChange - Callback when index changes
     * @returns {number} - New index
     */
    navigate(items, currentIndex, direction, onChange) {
        let newIndex = currentIndex + direction;
        
        if (newIndex < 0) {
            newIndex = items.length - 1;
        } else if (newIndex >= items.length) {
            newIndex = 0;
        }
        
        if (onChange) {
            onChange(items[newIndex], newIndex);
        }
        
        return newIndex;
    }
};

// Make utilities globally available
window.AjaxUtils = AjaxUtils;
window.UrlUtils = UrlUtils;
window.DomUtils = DomUtils;
window.ProductUtils = ProductUtils;
window.FormUtils = FormUtils;
window.CarouselUtils = CarouselUtils;
