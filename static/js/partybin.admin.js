// Funciones administrativas para dashboard party-bin
// Borrado masivo
function deleteSelected() {
  const checked = Array.from(document.querySelectorAll('.paste-check:checked')).map(cb => cb.value);
  if (checked.length === 0) return showToast('Selecciona al menos un paste.', 'warning');
  showConfirm(`¿Borrar ${checked.length} pastes?`, () => {
    fetch('/admin/delete-multi', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ids: checked})
    }).then(r=>r.json()).then(data=>{
      showToast(data.msg, data.status);
      if(data.status==='success') setTimeout(()=>location.reload(), 1200);
    });
  });
}
window.deleteSelected = deleteSelected;

// Filtro avanzado
function filterDashboard() {
  const q = document.getElementById('searchQ').value;
  const tag = document.getElementById('searchTag').value;
  const author = document.getElementById('searchAuthor').value;
  const type = document.getElementById('searchType').value;
  const url = `/dashboard?q=${encodeURIComponent(q)}&tag=${encodeURIComponent(tag)}&author=${encodeURIComponent(author)}&type=${encodeURIComponent(type)}`;
  window.location = url;
}
window.filterDashboard = filterDashboard;
