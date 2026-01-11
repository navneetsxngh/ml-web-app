let selectedFile = null;

// File input change handler
document.getElementById('fileInput').addEventListener('change', function(e) {
    selectedFile = e.target.files[0];
    if (selectedFile) {
        displayFileInfo();
    }
});

// Drag and drop handlers
const uploadBox = document.getElementById('uploadBox');

uploadBox.addEventListener('dragover', function(e) {
    e.preventDefault();
    uploadBox.style.borderColor = '#667eea';
    uploadBox.style.background = '#f7fafc';
});

uploadBox.addEventListener('dragleave', function(e) {
    e.preventDefault();
    uploadBox.style.borderColor = '#cbd5e0';
    uploadBox.style.background = 'white';
});

uploadBox.addEventListener('drop', function(e) {
    e.preventDefault();
    uploadBox.style.borderColor = '#cbd5e0';
    uploadBox.style.background = 'white';
    
    selectedFile = e.dataTransfer.files[0];
    if (selectedFile) {
        displayFileInfo();
    }
});

function displayFileInfo() {
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    
    fileName.textContent = `File name: ${selectedFile.name}`;
    fileSize.textContent = `File size: ${formatFileSize(selectedFile.size)}`;
    
    fileInfo.style.display = 'block';
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' bytes';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

function uploadFile() {
    if (!selectedFile) {
        showMessage('Please select a file first', 'error');
        return;
    }
    
    // Check file size (64MB limit)
    if (selectedFile.size > 64 * 1024 * 1024) {
        showMessage('File size exceeds 64MB limit', 'error');
        return;
    }
    
    // Check file extension
    const allowedExtensions = ['csv', 'json', 'xml'];
    const fileExtension = selectedFile.name.split('.').pop().toLowerCase();
    if (!allowedExtensions.includes(fileExtension)) {
        showMessage('Invalid file type. Only CSV, JSON, and XML are allowed.', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    // Show loading spinner
    document.getElementById('loadingSpinner').style.display = 'block';
    
    fetch('/upload_data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loadingSpinner').style.display = 'none';
        
        if (data.success) {
            showMessage(data.message, 'success');
            setTimeout(() => {
                window.location.href = '/visualization';
            }, 1500);
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        document.getElementById('loadingSpinner').style.display = 'none';
        showMessage('Error uploading file: ' + error.message, 'error');
    });
}

function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = message;
    messageDiv.className = 'message ' + type;
    messageDiv.style.display = 'block';
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}
