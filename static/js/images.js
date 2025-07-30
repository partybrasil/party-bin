// Vista previa automática de imágenes en el paste
function previewImages() {
  document.querySelectorAll('.paste-content img').forEach(img => {
    img.style.maxWidth = '100%';
    img.style.display = 'block';
    img.style.margin = '1em auto';
  });
}
document.addEventListener('DOMContentLoaded', previewImages);
