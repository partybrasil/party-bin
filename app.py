# --- INICIO DE PARTYBIN ---
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
import io
import json
import uuid
from datetime import datetime
import os
from config import DASHBOARD_SECRET

# Configuración básica
app = Flask(__name__)
app.secret_key = os.environ.get('PARTYBIN_SECRET', 'partybin_default_secret')

# Temas disponibles
THEMES = ['light', 'dark', 'hacker']
DEFAULT_THEME = 'light'

def get_theme():
	return session.get('theme', DEFAULT_THEME)

# Rutas principales
@app.route('/')
def index():
	return render_template('create.html', theme=get_theme())

@app.route('/create', methods=['GET', 'POST'])
def create_paste():
	if request.method == 'POST':
		data = request.form
		paste = {
			'title': data.get('title', ''),
			'content': data.get('content', ''),
			'format': data.get('format', 'markdown'),
			'url': data.get('custom_url') or uuid.uuid4().hex[:8],
			'password': data.get('password', ''),
			'author': data.get('author', ''),
			'tags': [t.strip() for t in data.get('tags', '').split(',') if t.strip()],
			'expiration': None,
			'autodestruct': data.get('autodestruct', 'none'),
			'autodestruct_value': data.get('autodestruct_value', ''),
			'max_views': None,
			'one_time': data.get('autodestruct', '') == 'one',
			'created_at': datetime.utcnow().isoformat(),
			'last_viewed': None,
			'views': 0,
			'edit_code': uuid.uuid4().hex[:10],
			'metadata': {}
		}
		# Guardar en JSON
		paste_path = os.path.join('data', 'pastes', f"{paste['url']}.json")
		with open(paste_path, 'w', encoding='utf-8') as f:
			json.dump(paste, f, ensure_ascii=False, indent=2)
		return redirect(url_for('view_paste', paste_url=paste['url']))
	return render_template('create.html', theme=get_theme())

@app.route('/view/<string:paste_url>')
def view_paste(paste_url):
    paste_path = os.path.join('data', 'pastes', f"{paste_url}.json")
    if not os.path.exists(paste_path):
        flash('Paste no encontrado', 'error')
        return redirect(url_for('index'))
    with open(paste_path, 'r', encoding='utf-8') as f:
        paste = json.load(f)
    # Si el paste es privado y no autenticado, mostrar solo metadatos y acciones
    if paste.get('privado') and not session.get(f'auth_{paste_url}', False):
        paste['rendered_content'] = None
        return render_template('view.html', paste=paste, theme=get_theme(), privado=True)
    # Renderizar contenido según formato
    if paste['format'] == 'markdown':
        try:
            import markdown2
            paste['rendered_content'] = markdown2.markdown(paste['content'])
        except:
            paste['rendered_content'] = paste['content']
    elif paste['format'] == 'html':
        paste['rendered_content'] = paste['content']
    elif paste['format'] == 'code':
        try:
            from pygments import highlight
            from pygments.lexers import guess_lexer
            from pygments.formatters import HtmlFormatter
            lexer = guess_lexer(paste['content'])
            paste['rendered_content'] = highlight(paste['content'], lexer, HtmlFormatter())
        except:
            paste['rendered_content'] = f"<pre>{paste['content']}</pre>"
    else:
        paste['rendered_content'] = f"<pre>{paste['content']}</pre>"
    return render_template('view.html', paste=paste, theme=get_theme(), privado=False)
# RAW
@app.route('/raw/<string:paste_url>', methods=['GET', 'POST'])
def raw_paste(paste_url):
    paste_path = os.path.join('data', 'pastes', f"{paste_url}.json")
    if not os.path.exists(paste_path):
        return "Paste not found", 404
    with open(paste_path, 'r', encoding='utf-8') as f:
        paste = json.load(f)
    if paste.get('privado') and not session.get(f'auth_{paste_url}', False):
        if request.method == 'POST':
            password = request.form.get('password', '')
            if paste['password'] and password == paste['password']:
                session[f'auth_{paste_url}'] = True
            else:
                return render_template('password_prompt.html', paste_url=paste_url, theme=get_theme())
        else:
            return render_template('password_prompt.html', paste_url=paste_url, theme=get_theme())
    return paste['content'], 200, {'Content-Type': 'text/plain; charset=utf-8'}

# EXPORT
@app.route('/export/<string:paste_url>', methods=['GET', 'POST'])
def export_paste(paste_url):
    export_type = request.args.get('type', 'txt')
    paste_path = os.path.join('data', 'pastes', f"{paste_url}.json")
    if not os.path.exists(paste_path):
        return "Paste not found", 404
    with open(paste_path, 'r', encoding='utf-8') as f:
        paste = json.load(f)
    if paste.get('privado') and not session.get(f'auth_{paste_url}', False):
        if request.method == 'POST':
            password = request.form.get('password', '')
            if paste['password'] and password == paste['password']:
                session[f'auth_{paste_url}'] = True
            else:
                return render_template('password_prompt.html', paste_url=paste_url, theme=get_theme())
        else:
            return render_template('password_prompt.html', paste_url=paste_url, theme=get_theme())
    filename = f"{paste_url}.{export_type}"
    if export_type == 'md':
        content = paste['content']
        mimetype = 'text/markdown'
    elif export_type == 'html':
        content = paste.get('rendered_content') or paste['content']
        mimetype = 'text/html'
    else:
        content = paste['content']
        mimetype = 'text/plain'
    return send_file(
        io.BytesIO(content.encode('utf-8')),
        mimetype=mimetype,
        as_attachment=True,
        download_name=filename
    )

# QR
@app.route('/qr/<string:paste_url>', methods=['GET', 'POST'])
def qr_paste(paste_url):
    paste_path = os.path.join('data', 'pastes', f"{paste_url}.json")
    if not os.path.exists(paste_path):
        return "Paste not found", 404
    with open(paste_path, 'r', encoding='utf-8') as f:
        paste = json.load(f)
    if paste.get('privado') and not session.get(f'auth_{paste_url}', False):
        if request.method == 'POST':
            password = request.form.get('password', '')
            if paste['password'] and password == paste['password']:
                session[f'auth_{paste_url}'] = True
            else:
                return render_template('password_prompt.html', paste_url=paste_url, theme=get_theme())
        else:
            return render_template('password_prompt.html', paste_url=paste_url, theme=get_theme())
    try:
        import qrcode
        import io
        paste_link = url_for('view_paste', paste_url=paste_url, _external=True)
        img = qrcode.make(paste_link)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return f"Error generando QR: {e}", 500

@app.route('/edit/<string:paste_url>', methods=['GET', 'POST'])
def edit_paste(paste_url):
    paste_path = os.path.join('data', 'pastes', f"{paste_url}.json")
    if not os.path.exists(paste_path):
        flash('Paste no encontrado', 'error')
        return redirect(url_for('index'))
    with open(paste_path, 'r', encoding='utf-8') as f:
        paste = json.load(f)
    # Si el paste es privado y no autenticado, pedir contraseña antes de mostrar el editor
    if paste.get('privado') and not session.get(f'auth_{paste_url}', False):
        return render_template('password_prompt.html', paste_url=paste_url, theme=get_theme())
    if request.method == 'POST':
        password = request.form.get('password', '')
        if paste['password']:
            if password != paste['password']:
                flash('Contraseña incorrecta', 'error')
                return render_template('edit.html', paste=paste, theme=get_theme())
        paste['title'] = request.form.get('title', paste['title'])
        paste['content'] = request.form.get('content', paste['content'])
        paste['format'] = request.form.get('format', paste['format'])
        paste['author'] = request.form.get('author', paste['author'])
        paste['tags'] = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
        paste['password'] = request.form.get('password', paste['password'])
        paste['autodestruct'] = request.form.get('autodestruct', paste['autodestruct'])
        paste['autodestruct_value'] = request.form.get('autodestruct_value', paste['autodestruct_value'])
        paste['privado'] = True if request.form.get('privado') == 'on' else False
        with open(paste_path, 'w', encoding='utf-8') as f:
            json.dump(paste, f, ensure_ascii=False, indent=2)
        flash('Paste editado correctamente', 'success')
        return redirect(url_for('view_paste', paste_url=paste_url))
    return render_template('edit.html', paste=paste, theme=get_theme())

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    authenticated = session.get('dashboard_auth', False)
    if request.method == 'POST':
        secret_key = request.form.get('secret_key', '')
        if secret_key == DASHBOARD_SECRET:
            session['dashboard_auth'] = True
            authenticated = True
            flash('Acceso concedido al dashboard', 'success')
        else:
            flash('Clave secreta incorrecta', 'error')
    if not authenticated:
        return render_template('dashboard.html', pastes=[], theme=get_theme())
    # Cargar todos los pastes
    pastes = []
    pastes_dir = os.path.join('data', 'pastes')
    for fname in os.listdir(pastes_dir):
        if fname.endswith('.json'):
            with open(os.path.join(pastes_dir, fname), 'r', encoding='utf-8') as f:
                paste = json.load(f)
                pastes.append(paste)
    return render_template('dashboard.html', pastes=pastes, theme=get_theme())
# --- FIN DE PARTYBIN ---
# Arranque local
@app.route('/set-theme/<string:theme>')
def set_theme(theme):
	if theme in THEMES:
		session['theme'] = theme
	return redirect(request.referrer or url_for('index'))

# --- Funciones administrativas del dashboard ---
import shutil
import zipfile
from io import BytesIO

# Cerrar sesión del dashboard
@app.route('/dashboard/logout', methods=['POST'])
def dashboard_logout():
    session.pop('dashboard_auth', None)
    flash('Sesión cerrada del dashboard', 'info')
    return redirect(url_for('dashboard'))

# Eliminar todos los pastes
@app.route('/dashboard/delete_all', methods=['POST'])
def dashboard_delete_all():
    if not session.get('dashboard_auth', False):
        flash('No autorizado', 'error')
        return redirect(url_for('dashboard'))
    pastes_dir = os.path.join('data', 'pastes')
    count = 0
    for fname in os.listdir(pastes_dir):
        if fname.endswith('.json'):
            os.remove(os.path.join(pastes_dir, fname))
            count += 1
    flash(f'Se eliminaron {count} pastes.', 'success')
    return redirect(url_for('dashboard'))

# Exportar todos los pastes como zip
@app.route('/dashboard/export_all', methods=['POST'])
def dashboard_export_all():
    if not session.get('dashboard_auth', False):
        flash('No autorizado', 'error')
        return redirect(url_for('dashboard'))
    pastes_dir = os.path.join('data', 'pastes')
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for fname in os.listdir(pastes_dir):
            if fname.endswith('.json'):
                zipf.write(os.path.join(pastes_dir, fname), arcname=fname)
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='partybin_pastes.zip')

# Eliminar paste individual
@app.route('/delete/<string:paste_url>', methods=['POST'])
def dashboard_delete_paste(paste_url):
    if not session.get('dashboard_auth', False):
        flash('No autorizado', 'error')
        return redirect(url_for('dashboard'))
    paste_path = os.path.join('data', 'pastes', f"{paste_url}.json")
    if os.path.exists(paste_path):
        os.remove(paste_path)
        flash('Paste eliminado correctamente.', 'success')
    else:
        flash('Paste no encontrado.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/auth/<string:paste_url>', methods=['POST'])
def auth_paste(paste_url):
    paste_path = os.path.join('data', 'pastes', f"{paste_url}.json")
    if not os.path.exists(paste_path):
        flash('Paste no encontrado', 'error')
        return redirect(url_for('index'))
    with open(paste_path, 'r', encoding='utf-8') as f:
        paste = json.load(f)
    password = request.form.get('password', '')
    if paste['password'] and password == paste['password']:
        session[f'auth_{paste_url}'] = True
        next_url = request.form.get('next', url_for('view_paste', paste_url=paste_url))
        return redirect(next_url)
    else:
        flash('Contraseña incorrecta', 'error')
        return render_template('password_prompt.html', paste_url=paste_url, theme=get_theme())
# Arranque local
if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5000)

