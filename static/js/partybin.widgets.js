// Toasts animados y utilidades visuales para party-bin
function showToast(msg, type = 'info', time = 3500) {
  const toast = document.createElement('div');
  toast.className = `toast align-items-center text-bg-${type} border-0 show animate__animated animate__fadeInUp`;
  toast.role = 'alert';
  toast.innerHTML = `<div class='d-flex'><div class='toast-body'>${msg}</div><button type='button' class='btn-close btn-close-white me-2 m-auto' data-bs-dismiss='toast'></button></div>`;
  document.body.appendChild(toast);
  setTimeout(() => { toast.classList.add('animate__fadeOutDown'); setTimeout(()=>toast.remove(), 800); }, time);
}
window.showToast = showToast;

// Modal de confirmación
function showConfirm(msg, onConfirm) {
  const modal = document.createElement('div');
  modal.className = 'modal fade show d-block';
  modal.tabIndex = -1;
  modal.innerHTML = `<div class='modal-dialog'><div class='modal-content'><div class='modal-header'><h5 class='modal-title'>Confirmar</h5><button type='button' class='btn-close' data-bs-dismiss='modal'></button></div><div class='modal-body'><p>${msg}</p></div><div class='modal-footer'><button type='button' class='btn btn-secondary' data-bs-dismiss='modal'>Cancelar</button><button type='button' class='btn btn-danger' id='confirmBtn'>Sí, continuar</button></div></div></div>`;
  document.body.appendChild(modal);
  modal.querySelector('.btn-secondary').onclick = () => modal.remove();
  modal.querySelector('.btn-close').onclick = () => modal.remove();
  modal.querySelector('#confirmBtn').onclick = () => { onConfirm(); modal.remove(); };
}
window.showConfirm = showConfirm;

// Tooltip y popover Bootstrap
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl);
});
const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl);
});
