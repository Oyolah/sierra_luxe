document.addEventListener('DOMContentLoaded', function() {
    const mainImageInput = document.querySelector('#mainImage');
    const mainImagePreview = document.querySelector('#mainImagePreview');
    const videoInput = document.querySelector('#productVideo');
    const videoPreview = document.querySelector('#videoPreview');
    const existingMainImage = mainImagePreview?.querySelector('img')?.src;
    const existingVideo = videoPreview?.querySelector('video')?.src;
    
    // Main image preview
    if (mainImageInput && mainImagePreview) {
        mainImageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    mainImagePreview.innerHTML = `
                        <img src="${e.target.result}" alt="Preview" class="img-fluid rounded" style="max-height: 150px;">
                    `;
                };
                reader.readAsDataURL(file);
            } else if (existingMainImage) {
                mainImagePreview.innerHTML = `
                    <img src="${existingMainImage}" alt="Current image" class="img-fluid rounded" style="max-height: 150px;">
                `;
            } else {
                mainImagePreview.innerHTML = `
                    <div class="bg-light rounded d-flex align-items-center justify-content-center" style="width: 150px; height: 150px;">
                        <span class="text-muted small">No image selected</span>
                    </div>
                `;
            }
        });
    }
    
    // Video preview
    if (videoInput && videoPreview) {
        videoInput.addEventListener('input', function(e) {
            const url = e.target.value;
            if (url) {
                videoPreview.innerHTML = `
                    <video src="${url}" controls class="img-fluid rounded" style="max-height: 150px;"></video>
                `;
            } else if (existingVideo) {
                videoPreview.innerHTML = `
                    <video src="${existingVideo}" controls class="img-fluid rounded" style="max-height: 150px;"></video>
                `;
            } else {
                videoPreview.innerHTML = `
                    <div class="bg-light rounded d-flex align-items-center justify-content-center" style="width: 150px; height: 150px;">
                        <span class="text-muted small">No video URL provided</span>
                    </div>
                `;
            }
        });
    }
});
