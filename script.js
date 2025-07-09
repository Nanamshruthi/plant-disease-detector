<script>
    // DOM elements
    const uploadBox = document.getElementById('uploadBox');
    const fileInput = document.getElementById('fileInput');
    const detectBtn = document.getElementById('detectBtn');
    const previewImage = document.getElementById('previewImage');
    const resultsSection = document.getElementById('resultsSection');
    
    // Disease detection results elements
    const diseaseResult = document.getElementById('diseaseResult');
    const confidenceResult = document.getElementById('confidenceResult');
    const recommendationResult = document.getElementById('recommendationResult');

    // Handle file selection
    uploadBox.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            const file = e.target.files[0];
            
            if (!file.type.match('image.*')) {
                alert('Please select an image file (JPEG, PNG, etc.)');
                return;
            }
            
            const reader = new FileReader();
            
            reader.onload = (event) => {
                previewImage.src = event.target.result;
                detectBtn.disabled = false;
            };
            
            reader.readAsDataURL(file);
        }
    });

    // Handle drag and drop
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('dragover');
    });

    uploadBox.addEventListener('dragleave', () => {
        uploadBox.classList.remove('dragover');
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('dragover');
        
        if (e.dataTransfer.files.length) {
            const file = e.dataTransfer.files[0];
            
            if (!file.type.match('image.*')) {
                alert('Please select an image file (JPEG, PNG, etc.)');
                return;
            }
            
            fileInput.files = e.dataTransfer.files;
            const reader = new FileReader();
            
            reader.onload = (event) => {
                previewImage.src = event.target.result;
                detectBtn.disabled = false;
            };
            
            reader.readAsDataURL(file);
        }
    });

    // Handle detection button click
    detectBtn.addEventListener('click', async () => {
        if (!fileInput.files.length) return;
        
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);
        
        detectBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        detectBtn.disabled = true;
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Display results
            diseaseResult.textContent = data.prediction;
            confidenceResult.textContent = data.confidence;
            recommendationResult.textContent = data.recommendation;
            
            // Update image preview with the uploaded version (in case it was resized)
            if (data.image_url) {
                previewImage.src = data.image_url;
            }
            
            resultsSection.classList.remove('hidden');
            
        } catch (error) {
            alert('Error: ' + error.message);
            console.error('Detection error:', error);
        } finally {
            detectBtn.innerHTML = '<i class="fas fa-search"></i> Detect Disease';
            detectBtn.disabled = false;
        }
    });
</script>