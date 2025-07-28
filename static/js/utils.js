// utils.js - Funciones JS para PartyBin
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Copiado al portapapeles');
    });
}
function updateWordCharCount(textareaId, wordCountId, charCountId) {
    const textarea = document.getElementById(textareaId);
    const wordCount = document.getElementById(wordCountId);
    const charCount = document.getElementById(charCountId);
    textarea.addEventListener('input', function() {
        const text = textarea.value;
        wordCount.textContent = text.trim().split(/\s+/).filter(Boolean).length;
        charCount.textContent = text.length;
    });
}
