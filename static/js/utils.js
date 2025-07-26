function copyToClipboard(text) {
    navigator.clipboard.writeText(text);
}
function updateWordCount(textarea, counterId) {
    var text = textarea.value;
    var words = text.trim().split(/\s+/).length;
    var chars = text.length;
    document.getElementById(counterId).innerText = `Palabras: ${words} | Caracteres: ${chars}`;
}
