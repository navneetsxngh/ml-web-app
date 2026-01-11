let columns = [];
let rows = [];

function createColumns() {
    const input = document.getElementById('columnNames').value.trim();
    if (!input) {
        showMessage('Please enter column names', 'error');
        return;
    }
    
    columns = input.split(',').map(col => col.trim()).filter(col => col);
    
    if (columns.length === 0) {
        showMessage('Please enter valid column names', 'error');
        return;
    }
    
    // Show data entry section
    document.getElementById('dataEntry').style.display = 'block';
    
    // Create row form
    createRowForm();
    
    // Update table headers
    updateTableHeaders();
    
    showMessage('Columns created successfully! Now add rows of data.', 'success');
}

function createRowForm() {
    const formHtml = columns.map((col, index) => `
        <div class="form-group" style="display: inline-block; margin-right: 15px;">
            <label>${col}:</label>
            <input type="text" id="col_${index}" class="form-control" style="width: 150px;">
        </div>
    `).join('');
    
    document.getElementById('rowForm').innerHTML = formHtml;
}

function updateTableHeaders() {
    const headersHtml = '<tr>' + columns.map(col => `<th>${col}</th>`).join('') + '</tr>';
    document.getElementById('tableHead').innerHTML = headersHtml;
}

function addRow() {
    const rowData = {};
    let isValid = true;
    
    columns.forEach((col, index) => {
        const value = document.getElementById(`col_${index}`).value.trim();
        if (!value) {
            isValid = false;
        }
        rowData[col] = value;
    });
    
    if (!isValid) {
        showMessage('Please fill all fields', 'error');
        return;
    }
    
    rows.push(rowData);
    updateTableBody();
    
    // Clear form
    columns.forEach((col, index) => {
        document.getElementById(`col_${index}`).value = '';
    });
    
    showMessage(`Row ${rows.length} added successfully!`, 'success');
}

function updateTableBody() {
    const bodyHtml = rows.map((row, index) => {
        const cells = columns.map(col => `<td>${row[col]}</td>`).join('');
        return `<tr>${cells}</tr>`;
    }).join('');
    
    document.getElementById('tableBody').innerHTML = bodyHtml;
}

function saveData() {
    if (rows.length === 0) {
        showMessage('Please add at least one row of data', 'error');
        return;
    }
    
    fetch('/create_csv', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            columns: columns,
            rows: rows
        })
    })
    .then(response => response.json())
    .then(data => {
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
