function toggleForm(btn, formId) {
    const panel = document.getElementById(formId);
    const isOpen = panel.classList.toggle('open');
    btn.textContent = isOpen ? '✕ Cancelar' : '+ Agregar';
}
