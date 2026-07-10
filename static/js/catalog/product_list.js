document.addEventListener('DOMContentLoaded', function() {
    const categoryFilter = document.querySelector('#categoryFilter');
    const minPrice = document.querySelector('#minPrice');
    const maxPrice = document.querySelector('#maxPrice');
    const sizeFilter = document.querySelector('#sizeFilter');
    const colorFilter = document.querySelector('#colorFilter');
    const applyFiltersBtn = document.querySelector('#applyFilters');
    const clearFiltersBtn = document.querySelector('#clearFilters');
    
    // Function to get filter parameters
    function getFilterParams() {
        const params = new URLSearchParams();
        
        if (categoryFilter && categoryFilter.value) params.set('category', categoryFilter.value);
        if (minPrice && minPrice.value) params.set('min_price', minPrice.value);
        if (maxPrice && maxPrice.value) params.set('max_price', maxPrice.value);
        if (sizeFilter && sizeFilter.value) params.set('size', sizeFilter.value);
        if (colorFilter && colorFilter.value) params.set('color', colorFilter.value);
        
        return params;
    }
    
    // Function to apply filters by reloading page with parameters
    function applyFilters() {
        const params = getFilterParams();
        const queryString = params.toString();
        const currentUrl = window.location.pathname;
        
        if (queryString) {
            window.location.href = currentUrl + '?' + queryString;
        } else {
            window.location.href = currentUrl;
        }
    }
    
    // Event listeners for filters
    applyFiltersBtn.addEventListener('click', applyFilters);
    
    clearFiltersBtn.addEventListener('click', function() {
        // Clear form values
        categoryFilter.value = '';
        minPrice.value = '';
        maxPrice.value = '';
        sizeFilter.value = '';
        colorFilter.value = '';
        
        // Reload page without parameters
        window.location.href = window.location.pathname;
    });
    
    // Auto-filter on category change
    categoryFilter.addEventListener('change', applyFilters);
});
