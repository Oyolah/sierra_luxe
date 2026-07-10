document.addEventListener('DOMContentLoaded', function() {
    const imageFilesInput = document.querySelector('#imageFiles');
    const imageFilesPreview = document.querySelector('#imageFilesPreview');
    const imageUploadArea = document.querySelector('#imageUploadArea');
    const videoFileInput = document.querySelector('#videoFile');
    const videoFilePreview = document.querySelector('#videoFilePreview');
    const existingVideo = videoFilePreview?.querySelector('video')?.src;
    
    // Initialize drag and drop for multiple images
    if (typeof initDragDrop === 'function') {
        initDragDrop('imageUploadArea', 'imageFiles', 'imageFilesPreview', null, true);
    }
    
    // Video preview
    if (videoFileInput && videoFilePreview) {
        videoFileInput.addEventListener('input', function(e) {
            const url = e.target.value;
            if (url) {
                videoFilePreview.innerHTML = `
                    <video src="${url}" controls class="img-fluid rounded" style="max-height: 150px;"></video>
                `;
            } else if (existingVideo) {
                videoFilePreview.innerHTML = `
                    <video src="${existingVideo}" controls class="img-fluid rounded" style="max-height: 150px;"></video>
                `;
            } else {
                videoFilePreview.innerHTML = `
                    <div class="bg-light rounded d-flex align-items-center justify-content-center" style="height: 100px;">
                        <span class="text-muted small">No video URL provided</span>
                    </div>
                `;
            }
        });
    }
});
