function updateAlgorithmOptions() {
    const algorithm = document.getElementById('algorithm').value;
    const infoDiv = document.getElementById('algorithmInfo');
    
    const descriptions = {
        'linear': 'Linear Regression: Best for continuous target variables with linear relationships. Predicts numeric values.',
        'ridge': 'Ridge Regression: Linear regression with L2 regularization. Helps prevent overfitting and handles multicollinearity.',
        'lasso': 'Lasso Regression: Linear regression with L1 regularization. Performs feature selection by shrinking some coefficients to zero.',
        'logistic': 'Logistic Regression: Best for binary classification problems. Predicts probabilities and class labels.'
    };
    
    if (algorithm && descriptions[algorithm]) {
        infoDiv.textContent = descriptions[algorithm];
        infoDiv.style.display = 'block';
    } else {
        infoDiv.style.display = 'none';
    }
}

function trainModel() {
    const algorithm = document.getElementById('algorithm').value;
    const target = document.getElementById('targetVariable').value;
    const testSize = document.getElementById('testSize').value;
    const randomState = document.getElementById('randomState').value;
    
    // Validation
    if (!algorithm) {
        showMessage('Please select an algorithm', 'error');
        return;
    }
    
    if (!target) {
        showMessage('Please select a target variable', 'error');
        return;
    }
    
    const testSizeNum = parseFloat(testSize);
    if (isNaN(testSizeNum) || testSizeNum <= 0 || testSizeNum >= 1) {
        showMessage('Test size must be between 0 and 1', 'error');
        return;
    }
    
    const randomStateNum = parseInt(randomState);
    if (isNaN(randomStateNum) || randomStateNum < 0) {
        showMessage('Random state must be a non-negative integer', 'error');
        return;
    }
    
    // Show loading
    document.getElementById('loadingSpinner').style.display = 'block';
    
    fetch('/training', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            algorithm: algorithm,
            target: target,
            test_size: testSizeNum,
            random_state: randomStateNum
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loadingSpinner').style.display = 'none';
        
        if (data.success) {
            displayMetrics(data.metrics, algorithm);
            document.getElementById('resultsSection').style.display = 'block';
            showMessage('Model trained successfully!', 'success');
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        document.getElementById('loadingSpinner').style.display = 'none';
        showMessage('Error: ' + error.message, 'error');
    });
}

function displayMetrics(metrics, algorithm) {
    const metricsDiv = document.getElementById('metricsDisplay');
    
    let html = '';
    
    if (algorithm === 'linear' || algorithm === 'ridge' || algorithm === 'lasso') {
        html = `
            <div class="metric-card">
                <div class="metric-label">R² Score</div>
                <div class="metric-value">${metrics.r2_score.toFixed(4)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Mean Squared Error</div>
                <div class="metric-value">${metrics.mse.toFixed(4)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Mean Absolute Error</div>
                <div class="metric-value">${metrics.mae.toFixed(4)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Root MSE</div>
                <div class="metric-value">${metrics.rmse.toFixed(4)}</div>
            </div>
        `;
    } else if (algorithm === 'logistic') {
        html = `
            <div class="metric-card">
                <div class="metric-label">Accuracy</div>
                <div class="metric-value">${(metrics.accuracy * 100).toFixed(2)}%</div>
            </div>
        `;
    }
    
    metricsDiv.innerHTML = html;
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
