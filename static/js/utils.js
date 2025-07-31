// Toast animado
function showToast(msg, type = 'info') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast animate__animated animate__fadeInUp bg-${type} text-white mb-2 p-3 rounded shadow`;
  toast.innerHTML = msg;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.remove('animate__fadeInUp');
    toast.classList.add('animate__fadeOutDown');
    setTimeout(() => toast.remove(), 1000);
  }, 3500);
}
// Cambia tema
function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  let link = document.getElementById('theme-link');
  link.href = `/static/themes/${theme}.css`;
}
