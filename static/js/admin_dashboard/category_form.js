document.addEventListener('DOMContentLoaded', function() {
    const imagePreview = document.querySelector('#imagePreview');
    const existingImageUrl = imagePreview?.querySelector('img')?.src;
    
    // Initialize drag and drop for category image
    if (typeof initDragDrop === 'function') {
        initDragDrop('categoryImageDropArea', 'categoryImage', 'imagePreview', existingImageUrl);
    }
});
