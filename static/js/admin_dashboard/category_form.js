document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.querySelector('#categoryImage');
    const imagePreview = document.querySelector('#imagePreview');
    const existingImageUrl = imagePreview?.querySelector('img')?.src;
    
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.innerHTML = `
                        <img src="${e.target.result}" alt="Preview" class="img-fluid rounded" style="max-height: 150px;">
                    `;
                };
                reader.readAsDataURL(file);
            } else if (existingImageUrl) {
                imagePreview.innerHTML = `
                    <img src="${existingImageUrl}" alt="Current image" class="img-fluid rounded" style="max-height: 150px;">
                `;
            } else {
                imagePreview.innerHTML = `
                    <div class="bg-light rounded d-flex align-items-center justify-content-center" style="width: 150px; height: 150px;">
                        <span class="text-muted small">No image selected</span>
                    </div>
                `;
            }
        });
    }
});
