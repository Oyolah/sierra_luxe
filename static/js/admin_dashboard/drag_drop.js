// Reusable Drag and Drop Utility
window.initDragDrop = function(dropAreaId, inputId, previewId, existingImage = null, isMultiple = false) {
    const dropArea = document.getElementById(dropAreaId);
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    
    if (!dropArea || !input || !preview) return;
    
    // Drag and drop event handlers
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight(e) {
        dropArea.classList.add('dragover');
    }
    
    function unhighlight(e) {
        dropArea.classList.remove('dragover');
    }
    
    dropArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        input.files = files;
        if (isMultiple) {
            handleMultipleFiles(files);
        } else {
            handleFile(files[0]);
        }
    }
    
    // File input change handler
    input.addEventListener('change', function(e) {
        const files = e.target.files;
        if (isMultiple) {
            handleMultipleFiles(files);
        } else {
            handleFile(files[0]);
        }
    });
    
    function handleFile(file) {
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.innerHTML = `
                    <img src="${e.target.result}" alt="Preview" class="img-fluid rounded" style="max-height: 150px;">
                `;
            };
            reader.readAsDataURL(file);
        } else if (existingImage) {
            preview.innerHTML = `
                <img src="${existingImage}" alt="Current image" class="img-fluid rounded" style="max-height: 150px;">
            `;
        } else {
            preview.innerHTML = `
                <div class="bg-light rounded d-flex align-items-center justify-content-center" style="width: 150px; height: 150px;">
                    <span class="text-muted small">No image selected</span>
                </div>
            `;
        }
    }
    
    function handleMultipleFiles(files) {
        if (files.length > 0) {
            preview.innerHTML = '';
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
                    preview.appendChild(col);
                };
                reader.readAsDataURL(file);
            });
        } else {
            preview.innerHTML = `
                <div class="col-12">
                    <div class="bg-light rounded d-flex align-items-center justify-content-center" style="height: 100px;">
                        <span class="text-muted small">No images selected</span>
                    </div>
                </div>
            `;
        }
    }
    
    // Expose removePreview function globally for multiple file handling
    window.removePreview = function(button, index) {
        const col = button.closest('.col-4');
        col.remove();
        
        // Update file input by creating a new FileList
        const currentFiles = Array.from(input.files);
        currentFiles.splice(index, 1);
        
        // Create a new DataTransfer object to set the files
        const dataTransfer = new DataTransfer();
        currentFiles.forEach(file => dataTransfer.items.add(file));
        input.files = dataTransfer.files;
        
        // Re-render previews with updated indices
        if (currentFiles.length > 0) {
            handleMultipleFiles(input.files);
        } else {
            preview.innerHTML = `
                <div class="col-12">
                    <div class="bg-light rounded d-flex align-items-center justify-content-center" style="height: 100px;">
                        <span class="text-muted small">No images selected</span>
                    </div>
                </div>
            `;
        }
    };
};
