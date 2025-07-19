let currentEditId = null;

// Initial loading
document.addEventListener('DOMContentLoaded', function() {
    loadItems();
    setupForm();
});

function setupForm() {
    const form = document.getElementById('item-form');
    form.addEventListener('submit', handleSubmit);
}

async function handleSubmit(event) {
    event.preventDefault();
    
    clearErrors();
    
    const formData = new FormData(event.target);
    const data = {
        name: formData.get('name'),
        mqtt_topic: formData.get('mqtt_topic'),
        unit: formData.get('unit'),
        duration: parseInt(formData.get('duration')),
        display_order: parseInt(formData.get('display_order')) || 0,
        is_active: formData.get('is_active') === 'on' // checkbox value
    };
    
    try {
        let response;
        if (currentEditId) {
            // Update
            response = await fetch(`/api/display_item/${currentEditId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
        } else {
            // Create
            response = await fetch('/api/display_item', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
        }
        
        if (response.ok) {
            showMessage('Item saved successfully!', 'success');
            resetForm();
            loadItems();
        } else {
            const errorData = await response.json();
            if (errorData.errors) {
                displayErrors(errorData.errors);
            } else {
                showMessage('Save error', 'error');
            }
        }
    } catch (error) {
        showMessage('Connection error', 'error');
        console.error('Error:', error);
    }
}

async function loadItems() {
    try {
        const response = await fetch('/api/display_item');
        const items = await response.json();
        
        const tbody = document.getElementById('items-table-body');
        tbody.innerHTML = '';
        
        // Sort by display_order
        items.sort((a, b) => a.display_order - b.display_order);
        
        items.forEach(item => {
            const row = document.createElement('tr');
            // Add class for inactive items
            if (!item.is_active) {
                row.classList.add('inactive-item');
            }
            
            row.innerHTML = `
                <th style="display: none;">${item.id}</th>
                <td>${escapeHtml(item.name)}</td>
                <td>${escapeHtml(item.mqtt_topic)}</td>
                <td>${escapeHtml(item.unit)}</td>
                <td>${item.duration}s</td>
                <td>${item.display_order}</td>
                <td>
                    <span class="status ${item.is_active ? 'active' : 'inactive'}">
                        ${item.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-secondary" onclick="editItem(${item.id})">Edit</button>
                    <button class="btn btn-danger" onclick="deleteItem(${item.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        showMessage('Error loading items', 'error');
        console.error('Error:', error);
    }
}

async function editItem(id) {
    try {
        const response = await fetch(`/api/display_item/${id}`);
        const item = await response.json();
        
        document.getElementById('item-id').value = item.id;
        document.getElementById('name').value = item.name;
        document.getElementById('mqtt_topic').value = item.mqtt_topic;
        document.getElementById('unit').value = item.unit;
        document.getElementById('duration').value = item.duration;
        document.getElementById('display_order').value = item.display_order;
        document.getElementById('is_active').checked = item.is_active;
        
        document.getElementById('form-title').textContent = 'Edit DisplayItem';
        document.getElementById('submit-btn').textContent = 'Update';
        
        currentEditId = id;
        
        // Scroll to form
        document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        showMessage('Error loading item', 'error');
        console.error('Error:', error);
    }
}

async function deleteItem(id) {
    if (!confirm('Are you sure you want to delete this item?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/display_item/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage('Item deleted successfully!', 'success');
            loadItems();
        } else {
            const errorData = await response.json();
            showMessage(`Delete error: ${errorData.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        showMessage('Connection error', 'error');
        console.error('Error:', error);
    }
}

function cancelEdit() {
    resetForm();
}

function resetForm() {
    document.getElementById('item-form').reset();
    // Reset default values
    document.getElementById('display_order').value = 0;
    document.getElementById('is_active').checked = true;
    
    document.getElementById('form-title').textContent = 'Add DisplayItem';
    document.getElementById('submit-btn').textContent = 'Add';
    currentEditId = null;
    clearErrors();
}

function clearErrors() {
    const errorElements = document.querySelectorAll('.error');
    errorElements.forEach(element => {
        element.textContent = '';
    });
}

function displayErrors(errors) {
    Object.keys(errors).forEach(field => {
        const errorElement = document.getElementById(`${field}-error`);
        if (errorElement) {
            errorElement.textContent = errors[field];
        }
    });
}

function showMessage(message, type) {
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML = `<div class="${type}" style="padding: 10px; margin: 10px 0; border-radius: 4px; background-color: ${type === 'success' ? '#d4edda' : '#f8d7da'};">${message}</div>`;
    
    // Remove message after 5 seconds
    setTimeout(() => {
        messagesDiv.innerHTML = '';
    }, 5000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
