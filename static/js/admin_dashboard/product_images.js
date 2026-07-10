document.addEventListener('DOMContentLoaded', function() {
    const imageFilesInput = document.querySelector('#imageFiles');
    const imageFilesPreview = document.querySelector('#imageFilesPreview');
    const imageUploadArea = document.querySelector('#imageUploadArea');
    const videoFileInput = document.querySelector('#videoFile');
    const videoFilePreview = document.querySelector('#videoFilePreview');
    const existingVideo = videoFilePreview?.querySelector('video')?.src;
    
    // Drag and drop functionality for image upload
    if (imageUploadArea && imageFilesInput) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            imageUploadArea.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            imageUploadArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            imageUploadArea.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight(e) {
            imageUploadArea.classList.add('dragover');
        }
        
        function unhighlight(e) {
            imageUploadArea.classList.remove('dragover');
        }
        
        imageUploadArea.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            imageFilesInput.files = files;
            handleFiles(files);
        }
    }
    
    // Multiple images preview
    if (imageFilesInput && imageFilesPreview) {
        imageFilesInput.addEventListener('change', function(e) {
            handleFiles(e.target.files);
        });
    }
    
    function handleFiles(files) {
        if (files.length > 0) {
            imageFilesPreview.innerHTML = '';
            Array.from(files).forEach((file, index) => {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const col = document.createElement('div');
                    col.className = 'col-4 position-relative';
                    col.innerHTML = `
                        <img src="${e.target.result}" alt="Preview" class="img-fluid rounded" style="height: 80px; object-fit: cover;">
                        <button type="button" class="preview-remove-btn" onclick="removePreview(this, ${index})">
                            <i class="fas fa-times"></i>
                        </button>
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
    }
    
    // Remove preview item
    window.removePreview = function(button, index) {
        const col = button.closest('.col-4');
        col.remove();
        
        // Update file input by creating a new FileList
        const currentFiles = Array.from(imageFilesInput.files);
        currentFiles.splice(index, 1);
        
        // Create a new DataTransfer object to set the files
        const dataTransfer = new DataTransfer();
        currentFiles.forEach(file => dataTransfer.items.add(file));
        imageFilesInput.files = dataTransfer.files;
        
        // Re-render previews with updated indices
        if (currentFiles.length > 0) {
            handleFiles(imageFilesInput.files);
        } else {
            imageFilesPreview.innerHTML = `
                <div class="col-12">
                    <div class="bg-light rounded d-flex align-items-center justify-content-center" style="height: 100px;">
                        <span class="text-muted small">No images selected</span>
                    </div>
                </div>
            `;
        }
    };
    
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
