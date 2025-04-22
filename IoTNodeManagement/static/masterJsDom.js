document.addEventListener('DOMContentLoader', function(){
   //GetElement
    const lieuModal = document.getElementById('lieu-modal');
    const microodal = document.getElementById('micro-modal');
    const addLieuBtn = document.getElementById('add-lieu-btn');
    const addMicroBtn = document.getElementById('add-micro-btn');
    const refreshBtn = document.getElementById('refresh-btn');
    const closeButtons = document.querySelectorAll('.close');

    // EventListeners
    addLieuBtn.addEventListener('click',() => openModal('lieu'));
    addMicroBtn.addEventListener('click',()=> openModal('micro'));
    refreshBtn.addEventListener('click',()=> refreshData());

    closeButtons.forEach((btn)=>{
        btn.addEventListener('click',()=>{
            lieuModal.style.display = 'none';
            microodal.style.display = 'none';
        })

    })

    //Form Submissions
    
    document.getElementById('lieu-form').addEventListener('submit',handleLieuSubmit);
    document.getElementById('micro-form').addEventListener('submit',handleMicroSubmit);

    window.addEventListener('click',(event) =>{
        if(event.target == lieuModal) lieuModal.style.display = 'none';
        if(event.target == microModal) microModal.style.display ='none';
    })

})

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