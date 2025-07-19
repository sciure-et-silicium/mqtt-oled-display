let currentEditId = null;

// Chargement initial
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
            // Mise à jour
            response = await fetch(`/api/display_item/${currentEditId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
        } else {
            // Création
            response = await fetch('/api/display_item', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
        }
        
        if (response.ok) {
            showMessage('Item sauvegardé avec succès !', 'success');
            resetForm();
            loadItems();
        } else {
            const errorData = await response.json();
            if (errorData.errors) {
                displayErrors(errorData.errors);
            } else {
                showMessage('Erreur lors de la sauvegarde', 'error');
            }
        }
    } catch (error) {
        showMessage('Erreur de connexion', 'error');
        console.error('Error:', error);
    }
}

async function loadItems() {
    try {
        const response = await fetch('/api/display_item');
        const items = await response.json();
        
        const tbody = document.getElementById('items-table-body');
        tbody.innerHTML = '';
        
        // Trier par display_order
        items.sort((a, b) => a.display_order - b.display_order);
        
        items.forEach(item => {
            const row = document.createElement('tr');
            // Ajouter une classe pour les items inactifs
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
                        ${item.is_active ? 'Actif' : 'Inactif'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-secondary" onclick="editItem(${item.id})">Éditer</button>
                    <button class="btn btn-danger" onclick="deleteItem(${item.id})">Supprimer</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        showMessage('Erreur lors du chargement des items', 'error');
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
        
        document.getElementById('form-title').textContent = 'Modifier un DisplayItem';
        document.getElementById('submit-btn').textContent = 'Modifier';
        
        currentEditId = id;
        
        // Scroll vers le formulaire
        document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        showMessage('Erreur lors du chargement de l\'item', 'error');
        console.error('Error:', error);
    }
}

async function deleteItem(id) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cet item ?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/display_item/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage('Item supprimé avec succès !', 'success');
            loadItems();
        } else {
            const errorData = await response.json();
            showMessage(`Erreur lors de la suppression: ${errorData.error || 'Erreur inconnue'}`, 'error');
        }
    } catch (error) {
        showMessage('Erreur de connexion', 'error');
        console.error('Error:', error);
    }
}

function cancelEdit() {
    resetForm();
}

function resetForm() {
    document.getElementById('item-form').reset();
    // Remettre les valeurs par défaut
    document.getElementById('display_order').value = 0;
    document.getElementById('is_active').checked = true;
    
    document.getElementById('form-title').textContent = 'Ajouter un DisplayItem';
    document.getElementById('submit-btn').textContent = 'Ajouter';
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
    
    // Supprimer le message après 5 secondes
    setTimeout(() => {
        messagesDiv.innerHTML = '';
    }, 5000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
