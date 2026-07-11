// Common Admin Dashboard JavaScript

// Initialize checkbox selection for tables
function initCheckboxSelection(selectAllId, checkboxClass) {
    const selectAllCheckbox = document.getElementById(selectAllId);
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('.' + checkboxClass);
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
    }
    
    const checkboxes = document.querySelectorAll('.' + checkboxClass);
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const allChecked = Array.from(checkboxes).every(cb => cb.checked);
            if (selectAllCheckbox) {
                selectAllCheckbox.checked = allChecked;
            }
        });
    });
}

// Auto-initialize checkbox selection when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Auto-initialize any checkbox groups
    const selectAllCheckboxes = document.querySelectorAll('[id^="select-all-"]');
    selectAllCheckboxes.forEach(selectAllCheckbox => {
        const selectAllId = selectAllCheckbox.id;
        const checkboxClass = selectAllId.replace('select-all-', '') + '-checkbox';
        initCheckboxSelection(selectAllId, checkboxClass);
    });
});
