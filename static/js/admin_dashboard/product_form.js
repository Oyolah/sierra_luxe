document.addEventListener('DOMContentLoaded', function() {
    const mainImagePreview = document.querySelector('#mainImagePreview');
    const existingMainImage = mainImagePreview?.querySelector('img')?.src;
    const videoInput = document.querySelector('#productVideo');
    const videoPreview = document.querySelector('#videoPreview');
    const existingVideo = videoPreview?.querySelector('video')?.src;
    
    // Initialize drag and drop for main image
    if (typeof initDragDrop === 'function') {
        initDragDrop('mainImageDropArea', 'mainImage', 'mainImagePreview', existingMainImage);
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
