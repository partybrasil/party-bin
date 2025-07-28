// Tabs logic
const tabText = document.getElementById('tab-text');
const tabPreview = document.getElementById('tab-preview');
const tabHow = document.getElementById('tab-how');
const tabContentText = document.getElementById('tab-content-text');
const tabContentPreview = document.getElementById('tab-content-preview');
const tabContentHow = document.getElementById('tab-content-how');
const textarea = document.getElementById('paste-text');

function showTab(tab) {
    tabContentText.style.display = 'none';
    tabContentPreview.style.display = 'none';
    tabContentHow.style.display = 'none';
    tabText.classList.remove('active');
    tabPreview.classList.remove('active');
    tabHow.classList.remove('active');
    if (tab === 'text') {
        tabContentText.style.display = 'block';
        tabText.classList.add('active');
    } else if (tab === 'preview') {
        tabContentPreview.style.display = 'block';
        tabPreview.classList.add('active');
        fetchPreview();
    } else if (tab === 'how') {
        tabContentHow.style.display = 'block';
        tabHow.classList.add('active');
    }
}

tabText.onclick = () => showTab('text');
tabPreview.onclick = () => showTab('preview');
tabHow.onclick = () => showTab('how');

function fetchPreview() {
    const text = textarea.value;
    fetch('/preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    })
    .then(res => res.text())
    .then(html => {
        tabContentPreview.innerHTML = html;
    });
}

// Metadata toggle
function toggleMetadata() {
    const fields = document.getElementById('metadata-fields');
    fields.style.display = fields.style.display === 'none' ? 'flex' : 'none';
}
