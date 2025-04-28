function showModal(title, message, type = 'success') {
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modal-title');
    const modalMessage = document.getElementById('modal-message');

    modalTitle.textContent = title;
    modalMessage.textContent = message;
    modal.classList.add('show', type);
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.classList.remove('show', 'success', 'error');
    if (modal.dataset.redirect) {
        window.location.href = modal.dataset.redirect;
    }
}

function updateModalStatus(stage, isComplete = false) {
    const statusElement = document.getElementById(`${stage}Status`);
    if (statusElement) {
        statusElement.classList.toggle('completed', isComplete);
        if (isComplete) {
            statusElement.querySelector('.status-icon').textContent += ' ✓';
        }
    }
}
