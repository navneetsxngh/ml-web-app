function toggleSelectAll() {
    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.column-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAll.checked;
    });
}

function getValueCounts() {
    const checkboxes = document.querySelectorAll('.column-checkbox:checked');
    const selectedColumns = Array.from(checkboxes).map(cb => cb.value);
    
    if (selectedColumns.length === 0) {
        showMessage('Please select at least one column', 'error');
        return;
    }
    
    fetch('/get_value_counts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            columns: selectedColumns
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayValueCounts(data.data);
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('Error: ' + error.message, 'error');
    });
}

function displayValueCounts(data) {
    const resultDiv = document.getElementById('valueCountsResult');
    
    let html = '';
    for (const [column, values] of Object.entries(data)) {
        html += `
            <div class="viz-section">
                <h3>${column}</h3>
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Value</th>
                                <th>Count</th>
                            </tr>
                        </thead>
                        <tbody>
        `;
        
        for (const [value, count] of Object.entries(values)) {
            html += `
                <tr>
                    <td>${value}</td>
                    <td>${count}</td>
                </tr>
            `;
        }
        
        html += `
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }
    
    resultDiv.innerHTML = html;
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
