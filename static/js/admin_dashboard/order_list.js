function applyFilters() {
    const params = new URLSearchParams();
    const search = document.querySelector('#searchInput').value;
    const status = document.querySelector('#statusFilter').value;
    
    if (search) params.set('search', search);
    if (status) params.set('status', status);
    
    window.location.href = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
}

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('#searchInput');
    const statusFilter = document.querySelector('#statusFilter');
    
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') applyFilters();
        });
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', applyFilters);
    }
});
