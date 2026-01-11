document.getElementById('predictionForm').addEventListener('submit', function(e) {
    e.preventDefault();
    makePrediction();
});

function makePrediction() {
    const form = document.getElementById('predictionForm');
    const formData = new FormData(form);
    
    const values = {};
    for (let [key, value] of formData.entries()) {
        values[key] = parseFloat(value);
        
        if (isNaN(values[key])) {
            showMessage(`Invalid value for ${key}. Please enter a numeric value.`, 'error');
            return;
        }
    }
    
    // Show loading
    document.getElementById('loadingSpinner').style.display = 'block';
    
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ values: values })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loadingSpinner').style.display = 'none';
        
        if (data.success) {
            displayPrediction(data.prediction);
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        document.getElementById('loadingSpinner').style.display = 'none';
        showMessage('Error: ' + error.message, 'error');
    });
}

function displayPrediction(prediction) {
    document.getElementById('predictionValue').textContent = prediction.toFixed(4);
    document.getElementById('predictionResult').style.display = 'block';
    
    // Scroll to result
    document.getElementById('predictionResult').scrollIntoView({ behavior: 'smooth' });
}

function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('predictionResult').style.display = 'none';
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
