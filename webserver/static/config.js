let currentEditKey = null;

document.addEventListener('DOMContentLoaded', function() {
    loadConfigs();
    setupForm();
});

function setupForm() {
    const form = document.getElementById('config-form');
    form.addEventListener('submit', handleSubmit);
}

async function handleSubmit(event) {
    event.preventDefault();
    
    clearErrors();
    
    const formData = new FormData(event.target);
    const data = {
        value: formData.get('value'),
        description: formData.get('description') || ''
    };
    
    try {
        const response = await fetch(`/api/config/${encodeURIComponent(currentEditKey)}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showMessage('Configuration mise à jour avec succès !', 'success');
            loadConfigs();
            // Garder le formulaire ouvert avec les nouvelles valeurs
            const updatedConfig = await response.json();
            document.getElementById('value').value = updatedConfig.value;
            document.getElementById('description').value = updatedConfig.description || '';
        } else {
            const errorData = await response.json();
            if (errorData.errors) {
                displayErrors(errorData.errors);
            } else {
                showMessage(`Erreur : ${errorData.error || 'Erreur inconnue'}`, 'error');
            }
        }
    } catch (error) {
        showMessage('Erreur de connexion', 'error');
        console.error('Error:', error);
    }
}

async function loadConfigs() {
    try {
        const response = await fetch('/api/config');
        const configs = await response.json();
        
        const tbody = document.getElementById('config-table-body');
        tbody.innerHTML = '';
        
        configs.forEach(config => {
            const row = document.createElement('tr');
            if (currentEditKey === config.key) {
                row.classList.add('editing');
            }
            
            row.innerHTML = `
                <td><code>${escapeHtml(config.key)}</code></td>
                <td class="config-value">${escapeHtml(config.value)}</td>
                <td class="config-description">${escapeHtml(config.description || '')}</td>
                <td>
                    <button class="btn btn-secondary" onclick="editConfig('${escapeHtml(config.key)}')">
                        ${currentEditKey === config.key ? 'En cours...' : 'Éditer'}
                    </button>
                </td>
            `;
            
            tbody.appendChild(row);
        });
        
    } catch (error) {
        showMessage('Erreur lors du chargement des configurations', 'error');
        console.error('Error:', error);
    }
}

async function editConfig(key) {
    try {
        const response = await fetch(`/api/config/${encodeURIComponent(key)}`);
        const config = await response.json();
        
        document.getElementById('key').value = config.key;
        document.getElementById('value').value = config.value;
        document.getElementById('description').value = config.description || '';
        
        currentEditKey = key;
        
        // Afficher le formulaire et masquer le message
        document.getElementById('config-form').style.display = 'block';
        document.getElementById('no-selection').style.display = 'none';
        
        // Scroll vers le formulaire
        document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
        
        // Recharger pour mettre à jour l'affichage des boutons
        loadConfigs();
        
    } catch (error) {
        showMessage('Erreur lors du chargement de la configuration', 'error');
        console.error('Error:', error);
    }
}

function cancelEdit() {
    resetForm();
}

function resetForm() {
    document.getElementById('config-form').reset();
    document.getElementById('config-form').style.display = 'none';
    document.getElementById('no-selection').style.display = 'block';
    currentEditKey = null;
    clearErrors();
    loadConfigs();
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
    
    setTimeout(() => {
        messagesDiv.innerHTML = '';
    }, 5000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
