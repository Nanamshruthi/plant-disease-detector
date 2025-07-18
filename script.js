document.addEventListener('DOMContentLoaded', function() {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const previewImage = document.getElementById('preview-image');
    const imagePreview = document.getElementById('image-preview');
    const detectBtn = document.getElementById('detect-btn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const removeBtn = document.getElementById('remove-btn');
    const browseBtn = document.querySelector('.browse-btn');
    const uploadContent = document.querySelector('.upload-content');

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.classList.add('highlight');
    }

    function unhighlight() {
        dropArea.classList.remove('highlight');
    }

    // Handle dropped files
    dropArea.addEventListener('drop', handleDrop, false);
    browseBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFiles);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles({ target: { files } });
    }

    function handleFiles(e) {
        const file = e.target.files[0];
        if (file && file.type.match('image.*')) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                imagePreview.style.display = 'block';
                uploadContent.style.opacity = '0';
                setTimeout(() => {
                    uploadContent.style.display = 'none';
                }, 300);
                detectBtn.disabled = false;
            };
            
            reader.readAsDataURL(file);
        }
    }

    // Remove image
    removeBtn.addEventListener('click', function() {
        previewImage.src = '';
        imagePreview.style.display = 'none';
        uploadContent.style.display = 'block';
        setTimeout(() => {
            uploadContent.style.opacity = '1';
        }, 10);
        detectBtn.disabled = true;
        fileInput.value = '';
        results.style.display = 'none';
    });

    // Detect disease
    detectBtn.addEventListener('click', detectDisease);

    function detectDisease() {
        loading.style.display = 'block';
        results.style.display = 'none';
        
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            displayResults({
                disease: 'Error',
                confidence: '0%',
                treatment: 'Failed to analyze the image. Please try again.'
            });
        })
        .finally(() => {
            loading.style.display = 'none';
        });
    }

    function displayResults(data) {
        document.getElementById('disease-result').textContent = data.disease || '-';
        document.getElementById('confidence-result').textContent = data.confidence || '-';
        document.getElementById('treatment-result').textContent = data.treatment || '-';
        
        // If you have a sample image for the detected disease
        if (data.sample_image) {
            document.getElementById('result-image').src = data.sample_image;
            document.querySelector('.result-image').style.display = 'block';
        } else {
            document.querySelector('.result-image').style.display = 'none';
        }
        
        results.style.display = 'block';
    }
});


