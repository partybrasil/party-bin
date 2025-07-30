// Funcionalidades avanzadas party-bin
// Expiración por cuenta regresiva
function startCountdown(expireAt) {
  const el = document.getElementById('countdown');
  if (!el) return;
  function update() {
    const now = new Date();
    const end = new Date(expireAt);
    let diff = Math.max(0, end-now);
    let s = Math.floor(diff/1000)%60;
    let m = Math.floor(diff/60000)%60;
    let h = Math.floor(diff/3600000)%24;
    let d = Math.floor(diff/86400000);
    el.textContent = `${d}d ${h}h ${m}m ${s}s`;
    if(diff>0) setTimeout(update, 1000);
  }
  update();
}
window.startCountdown = startCountdown;

// Notificaciones push
function notify(msg) {
  if (Notification && Notification.permission === 'granted') {
    new Notification('party-bin', {body: msg, icon: '/static/img/logo.png'});
  }
}
window.notify = notify;
