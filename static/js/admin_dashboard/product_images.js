document.addEventListener('DOMContentLoaded', function() {
    const imageFilesInput = document.querySelector('#imageFiles');
    const imageFilesPreview = document.querySelector('#imageFilesPreview');
    const videoFileInput = document.querySelector('#videoFile');
    const videoFilePreview = document.querySelector('#videoFilePreview');
    const existingVideo = videoFilePreview?.querySelector('video')?.src;
    
    // Multiple images preview
    if (imageFilesInput && imageFilesPreview) {
        imageFilesInput.addEventListener('change', function(e) {
            const files = e.target.files;
            if (files.length > 0) {
                imageFilesPreview.innerHTML = '';
                Array.from(files).forEach(file => {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const col = document.createElement('div');
                        col.className = 'col-4';
                        col.innerHTML = `
                            <img src="${e.target.result}" alt="Preview" class="img-fluid rounded" style="height: 80px; object-fit: cover;">
                        `;
                        imageFilesPreview.appendChild(col);
                    };
                    reader.readAsDataURL(file);
                });
            } else {
                imageFilesPreview.innerHTML = `
                    <div class="col-12">
                        <div class="bg-light rounded d-flex align-items-center justify-content-center" style="height: 100px;">
                            <span class="text-muted small">No images selected</span>
                        </div>
                    </div>
                `;
            }
        });
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
