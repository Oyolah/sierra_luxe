function updateBulkDeleteButton() {
    var checkboxes = document.querySelectorAll('.product-checkbox:checked');
    var bulkDeleteBtn = document.querySelector('#bulkDeleteBtn');
    if (bulkDeleteBtn) {
        bulkDeleteBtn.style.display = checkboxes.length > 0 ? 'inline-block' : 'none';
    }
}

function toggleSelectAll() {
    var selectAll = document.querySelector('#selectAll');
    var checkboxes = document.querySelectorAll('.product-checkbox');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = selectAll.checked;
    }
    updateBulkDeleteButton();
}

function bulkDelete() {
    var checkboxes = document.querySelectorAll('.product-checkbox:checked');
    if (checkboxes.length === 0) return;
    
    if (confirm('Are you sure you want to delete ' + checkboxes.length + ' product(s)?')) {
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = window.location.pathname.replace('list', 'bulk-delete');
        
        var csrfToken = document.createElement('input');
        csrfToken.type = 'hidden';
        csrfToken.name = 'csrfmiddlewaretoken';
        csrfToken.value = document.querySelector('[name=csrfmiddlewaretoken]').value;
        form.appendChild(csrfToken);
        
        for (var i = 0; i < checkboxes.length; i++) {
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'product_ids';
            input.value = checkboxes[i].value;
            form.appendChild(input);
        }
        
        document.body.appendChild(form);
        form.submit();
    }
}

function applyFilters() {
    var params = new URLSearchParams();
    var search = document.querySelector('#searchInput').value;
    var category = document.querySelector('#categoryFilter').value;
    var status = document.querySelector('#statusFilter').value;
    
    if (search) params.set('search', search);
    if (category) params.set('category', category);
    if (status) params.set('status', status);
    
    window.location.href = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
}

document.addEventListener('DOMContentLoaded', function() {
    updateBulkDeleteButton();
    
    const searchInput = document.querySelector('#searchInput');
    const categoryFilter = document.querySelector('#categoryFilter');
    const statusFilter = document.querySelector('#statusFilter');
    
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') applyFilters();
        });
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', applyFilters);
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', applyFilters);
    }
});
