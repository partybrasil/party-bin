// Previsualización en vivo y contador de palabras/caracteres
function updatePreview() {
  const content = document.getElementById('content').value;
  fetch('/preview', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content })
  })
    .then(r => r.text())
    .then(html => {
      document.getElementById('preview').innerHTML = html;
    });
}

function updateCounters() {
  const content = document.getElementById('content').value;
  document.getElementById('wordcount').textContent = content.trim().split(/\s+/).filter(Boolean).length;
  document.getElementById('charcount').textContent = content.length;
}

document.addEventListener('DOMContentLoaded', function() {
  const content = document.getElementById('content');
  if (content) {
    content.addEventListener('input', function() {
      updatePreview();
      updateCounters();
    });
    updatePreview();
    updateCounters();
  }
});
