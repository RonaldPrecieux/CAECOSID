document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const lieuModal = document.getElementById('lieu-modal');
    const microModal = document.getElementById('micro-modal');
    const addLieuBtn = document.getElementById('add-lieu-btn');
    const addMicroBtn = document.getElementById('add-micro-btn');
    const refreshBtn = document.getElementById('refresh-btn');
    const closeButtons = document.querySelectorAll('.close');
    
    // Event Listeners
    addLieuBtn.addEventListener('click', () => openModal('lieu'));
    addMicroBtn.addEventListener('click', () => openModal('micro'));
    refreshBtn.addEventListener('click', refreshData);
    
    closeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            lieuModal.style.display = 'none';
            microModal.style.display = 'none';
        });
    });
    
    // Form submissions
    document.getElementById('lieu-form').addEventListener('submit', handleLieuSubmit);
    document.getElementById('micro-form').addEventListener('submit', handleMicroSubmit);
    
    // Close modal when clicking outside
    window.addEventListener('click', (event) => {
        if (event.target === lieuModal) lieuModal.style.display = 'none';
        if (event.target === microModal) microModal.style.display = 'none';
    });
});

function openModal(type) {
    const modal = document.getElementById(`${type}-modal`);
    const title = document.getElementById(`modal-${type}-title`);
    const form = document.getElementById(`${type}-form`);
    
    // Reset form
    form.reset();
    
    // Set title and hidden field
    if (type === 'lieu') {
        title.textContent = 'Ajouter un Lieu';
        document.getElementById('lieu-id').value = '';
    } else {
        title.textContent = 'Ajouter un Microcontrôleur';
        document.getElementById('micro-uuid').value = '';
    }
    
    modal.style.display = 'flex';
}

async function handleLieuSubmit(e) {
    e.preventDefault();
    
    const id = document.getElementById('lieu-id').value;
    const nom = document.getElementById('lieu-nom').value;
    
    const url = id ? `/lieux/${id}` : '/lieux/';
    const method = id ? 'PUT' : 'POST';
    id?console.log(`id est la ${id}`):null

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nom ,id})
        });
        
        if (!response.ok) {
            const errorDetails = await response.json(); // Si le serveur renvoie des détails d'erreur
            console.error('Server Error:', errorDetails);throw new Error('Erreur lors de la requête')};
        
        refreshData();
        document.getElementById('lieu-modal').style.display = 'none';
    } catch (error) {
        console.error('Error:', error);
        alert('Une erreur est survenue');
    }
}
//POST and PUT
async function handleMicroSubmit(e) {
    e.preventDefault();
    
    const uuid = document.getElementById('micro-uuid').value || document.getElementById('micro-uuid-input').value;
    const uuid_cache = document.getElementById('micro-uuid').value;
    const nom = document.getElementById('micro-nom').value;
    const lieu_id = document.getElementById('micro-lieu').value || null;
    
    const url = document.getElementById('micro-uuid').value ? `/microcontroleurs/${uuid}` : '/microcontroleurs/';
    const method = document.getElementById('micro-uuid').value ? 'PUT' : 'POST';
   

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ uuid, nom, lieu_id })
        });
        
        if (!response.ok) { const errorDetails = await response.json(); // Si le serveur renvoie des détails d'erreur
            console.error('Server Error:', errorDetails);
            throw new Error('Erreur lors de la requête');}
        
        refreshData();
        document.getElementById('micro-modal').style.display = 'none';
    } catch (error) {
        console.error('Error:', error);
        alert('Une erreur est survenue');
    }
}

function editLieu(id) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    const nom = row.querySelector('td[data-field="nom"]').textContent;
    
    document.getElementById('lieu-id').value = id;
    document.getElementById('lieu-nom').value = nom;
    document.getElementById('modal-lieu-title').textContent = 'Modifier Lieu';
    
    document.getElementById('lieu-modal').style.display = 'flex';
}
function editMicro(uuid){

    const row = document.querySelector(`tr[data-uuid="${uuid}"]`);
    console.log("row trouvé ?", row);

    const lieu = document.querySelector(`tr[data-uuid="${uuid}"] td[data-field="lieu_id"]`).dataset['lieuId'] || "";
    //const nom = document.querySelector(`tr[data-uuid="${uuid}"] td[data-field="nom"]`).textContent;
    const nom = row.querySelector(`td[data-field="nom"]`).textContent;

    document.getElementById('modal-micro-title').textContent = "Modifier un Micro-controlleur" ;
    document.getElementById('micro-nom').value = nom;
    document.getElementById('micro-uuid-input').value = uuid;
    document.getElementById('micro-lieu').value = lieu;
    document.getElementById('micro-uuid').value = uuid;
    document.getElementById('micro-modal').style.display = 'flex';



}

async function deleteLieu(id) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce lieu?')) return;
    
    try {
        const response = await fetch(`/lieux/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Erreur lors de la suppression');
        
        refreshData();
    } catch (error) {
        console.error('Error:', error);
        alert('Une erreur est survenue lors de la suppression');
    }
}

async function deleteMicro(uuid) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce microcontrôleur?')) return;
    
    try {
        const response = await fetch(`/microcontroleurs/${uuid}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Erreur lors de la suppression');
        
        refreshData();
    } catch (error) {
        console.error('Error:', error);
        alert('Une erreur est survenue lors de la suppression');
    }
}

function refreshData() {
    window.location.reload();
}