// Toasts animados y utilidades admin para party-bin
function showToast(msg, type='info') {
  const toast = document.createElement('div');
  toast.className = `toast align-items-center text-bg-${type} border-0 show animate__animated animate__fadeInUp`;
  toast.role = 'alert';
  toast.innerHTML = `<div class='d-flex'><div class='toast-body'>${msg}</div><button type='button' class='btn-close btn-close-white me-2 m-auto' data-bs-dismiss='toast'></button></div>`;
  document.body.appendChild(toast);
  setTimeout(()=>toast.classList.add('animate__fadeOutDown'), 3500);
  setTimeout(()=>toast.remove(), 4000);
}
window.showToast = showToast;

// Confirmación modal para acciones peligrosas
function confirmAction(msg, cb) {
  if (window.confirm(msg)) cb();
}
window.confirmAction = confirmAction;

// Selección múltiple en dashboard
function toggleSelectAll(checked) {
  document.querySelectorAll('.paste-select').forEach(e=>e.checked=checked);
}
window.toggleSelectAll = toggleSelectAll;

// Borrado masivo
function deleteSelected(url) {
  const ids = Array.from(document.querySelectorAll('.paste-select:checked')).map(e=>e.value);
  if (!ids.length) return showToast('Selecciona al menos un paste', 'warning');
  confirmAction('¿Seguro que quieres borrar los seleccionados?', ()=>{
    fetch(url, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ids})})
      .then(r=>r.json()).then(d=>{showToast(d.msg, d.status); location.reload();});
  });
}
window.deleteSelected = deleteSelected;
