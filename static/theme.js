const themeToggle = document.getElementById('theme-toggle');
themeToggle.onclick = function() {
    document.body.classList.toggle('dark-mode');
    document.body.classList.toggle('light-mode');
    themeToggle.textContent = document.body.classList.contains('dark-mode') ? '🌙' : '☀️';
}
