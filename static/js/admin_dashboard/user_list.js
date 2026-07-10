function applyFilters() {
    const params = new URLSearchParams();
    const search = document.querySelector('#searchInput').value;
    const role = document.querySelector('#roleFilter').value;
    
    if (search) params.set('search', search);
    if (role) params.set('role', role);
    
    window.location.href = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
}

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('#searchInput');
    const roleFilter = document.querySelector('#roleFilter');
    
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') applyFilters();
        });
    }
    
    if (roleFilter) {
        roleFilter.addEventListener('change', applyFilters);
    }
});
