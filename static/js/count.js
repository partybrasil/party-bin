// Contador de palabras y caracteres en tiempo real
function updateCount() {
  const textarea = document.getElementById('content');
  const wordCount = document.getElementById('wordCount');
  const charCount = document.getElementById('charCount');
  if (!textarea || !wordCount || !charCount) return;
  const text = textarea.value;
  wordCount.textContent = text.trim().split(/\s+/).filter(Boolean).length;
  charCount.textContent = text.length;
}
document.addEventListener('DOMContentLoaded', function() {
  const textarea = document.getElementById('content');
  if (textarea) {
    textarea.addEventListener('input', updateCount);
    updateCount();
  }
});
