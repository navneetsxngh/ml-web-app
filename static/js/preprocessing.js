function toggleSelectAllOutliers() {
    const selectAll = document.getElementById('selectAllOutliers');
    const checkboxes = document.querySelectorAll('.outlier-checkbox');
    checkboxes.forEach(cb => cb.checked = selectAll.checked);
}

function toggleSelectAllEncoding() {
    const selectAll = document.getElementById('selectAllEncoding');
    const checkboxes = document.querySelectorAll('.encoding-checkbox');
    checkboxes.forEach(cb => cb.checked = selectAll.checked);
}

function toggleSelectAllScaling() {
    const selectAll = document.getElementById('selectAllScaling');
    const checkboxes = document.querySelectorAll('.scaling-checkbox');
    checkboxes.forEach(cb => cb.checked = selectAll.checked);
}

function handleMissing() {
    const method = document.getElementById('missingMethod').value;
    
    if (!method) {
        showMessage('Please select a method', 'error');
        return;
    }
    
    document.getElementById('loadingSpinner').style.display = 'block';
    
    fetch('/handle_missing', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ method: method })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loadingSpinner').style.display = 'none';
        
        if (data.success) {
            showMessage(data.message, 'success');
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        document.getElementById('loadingSpinner').style.display = 'none';
        showMessage('Error: ' + error.message, 'error');
    });
}

function visualizeOutliers() {
    const checkboxes = document.querySelectorAll('.outlier-checkbox:checked');
    const selectedColumns = Array.from(checkboxes).map(cb => cb.value);
    
    if (selectedColumns.length === 0) {
        showMessage('Please select at least one column', 'error');
        return;
    }
    
    document.getElementById('loadingSpinner').style.display = 'block';
    
    fetch('/visualize_outliers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ columns: selectedColumns })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loadingSpinner').style.display = 'none';
        
        if (data.success) {
            const vizDiv = document.getElementById('outlierVisualization');
            vizDiv.innerHTML = `
                <div class="image-container">
                    <img src="data:image/png;base64,${data.image}" alt="Outlier Visualization">
                </div>
            `;
            showMessage('Outliers visualized successfully', 'success');
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        document.getElementById('loadingSpinner').style.display = 'none';
        showMessage('Error: ' + error.message, 'error');
    });
}

function handleOutliers() {
    const checkboxes = document.querySelectorAll('.outlier-checkbox:checked');
    const selectedColumns = Array.from(checkboxes).map(cb => cb.value);
    const method = document.getElementById('outlierMethod').value;
    
    if (selectedColumns.length === 0) {
        showMessage('Please select at least one column', 'error');
        return;
    }
    
    if (!method) {
        showMessage('Please select a handling method', 'error');
        return;
    }
    
    document.getElementById('loadingSpinner').style.display = 'block';
    
    fetch('/handle_outliers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            columns: selectedColumns,
            method: method
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loadingSpinner').style.display = 'none';
        
        if (data.success) {
            const resultDiv = document.getElementById('outlierResult');
            resultDiv.innerHTML = `
                <h3>Before & After Comparison</h3>
                <div class="image-container">
                    <img src="data:image/png;base64,${data.image}" alt="Outlier Handling Result">
                </div>
            `;
            showMessage(data.message, 'success');
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        document.getElementById('loadingSpinner').style.display = 'none';
        showMessage('Error: ' + error.message, 'error');
    });
}

function encodeData() {
    const checkboxes = document.querySelectorAll('.encoding-checkbox:checked');
    const selectedColumns = Array.from(checkboxes).map(cb => cb.value);
    const method = document.getElementById('encodingMethod').value;
    
    if (selectedColumns.length === 0) {
        showMessage('Please select at least one column', 'error');
        return;
    }
    
    if (!method) {
        showMessage('Please select an encoding method', 'error');
        return;
    }
    
    document.getElementById('loadingSpinner').style.display = 'block';
    
    fetch('/encode_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            columns: selectedColumns,
            method: method
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loadingSpinner').style.display = 'none';
        
        if (data.success) {
            showMessage(data.message, 'success');
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        document.getElementById('loadingSpinner').style.display = 'none';
        showMessage('Error: ' + error.message, 'error');
    });
}

function scaleData() {
    const checkboxes = document.querySelectorAll('.scaling-checkbox:checked');
    const selectedColumns = Array.from(checkboxes).map(cb => cb.value);
    const method = document.getElementById('scalingMethod').value;
    
    if (selectedColumns.length === 0) {
        showMessage('Please select at least one column', 'error');
        return;
    }
    
    if (!method) {
        showMessage('Please select a scaling method', 'error');
        return;
    }
    
    document.getElementById('loadingSpinner').style.display = 'block';
    
    fetch('/scale_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            columns: selectedColumns,
            method: method
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loadingSpinner').style.display = 'none';
        
        if (data.success) {
            showMessage(data.message, 'success');
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        document.getElementById('loadingSpinner').style.display = 'none';
        showMessage('Error: ' + error.message, 'error');
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
