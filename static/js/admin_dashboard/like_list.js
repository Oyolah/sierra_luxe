document.addEventListener('DOMContentLoaded', function() {
    // Select all likes checkbox
    const selectAllLikes = document.getElementById('select-all-likes');
    if (selectAllLikes) {
        selectAllLikes.addEventListener('change', function() {
            const likeCheckboxes = document.querySelectorAll('.like-checkbox');
            likeCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
    }
    
    // Update select all checkbox when individual checkboxes change
    const likeCheckboxes = document.querySelectorAll('.like-checkbox');
    likeCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const allChecked = Array.from(likeCheckboxes).every(cb => cb.checked);
            if (selectAllLikes) {
                selectAllLikes.checked = allChecked;
            }
        });
    });
});
