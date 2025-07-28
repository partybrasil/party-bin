# 👇 PROMPT MAESTRO PARA COPILOT – PARTYBIN

"""
📌 CONTEXTO DEL PROYECTO:

Este repositorio contiene PartyBin, una aplicación web desarrollada en Python con Flask, diseñada como un clon personalizado de Rentry.org, pero con muchas funciones avanzadas añadidas.

🧠 TU TAREA (GitHub Copilot + Visual Studio Code):

Lee cuidadosamente el archivo README.md de este repositorio.
A partir de la descripción completa allí incluida, **genera la estructura de carpetas, archivos y lógica necesaria** para que PartyBin funcione exactamente como se especifica, sin añadir ni omitir funcionalidades.

✅ FUNCIONALIDADES CLAVE A RESPETAR:

- Crear y editar pastes en texto plano, Markdown o código con resaltado de sintaxis (auto o definido).
- URLs personalizadas o aleatorias al crear pastes.
- Expiración automática por tiempo/fecha o por número de vistas.
- Protección con contraseña (edición y/o visualización).
- Firma opcional, contador de palabras, tags, y metadatos.
- Temas visuales seleccionables (claro, oscuro, hacker).
- Dashboard local sin login, acceso por clave secreta.
- Exportación y visualización raw/copia/Qr/descarga.
- Estructura modular y liviana, con mínimo consumo de recursos.
- Capacidad de funcionar tanto en local como en Render.com.
- Pastes locales y online están desacoplados por seguridad.

📁 TU OBJETIVO:

1. Crea la estructura básica: `app.py`, `templates/`, `static/`, `data/pastes/`, etc.
2. Implementa la lógica del servidor y renderizado en Flask.
3. Usa Markdown2, Pygments, Jinja2, y otras libs necesarias.
4. Asegúrate de que cada componente del README.md se refleje en el código.
5. La prioridad es **modularidad, legibilidad y precisión funcional**.

💡 Recuerda:
- El README.md ya lo define todo. **No inventes ni asumas cosas fuera del documento.**
- Mantén el código limpio y bien comentado. Usa funciones reutilizables y evita duplicar lógica.

🔚 Una vez que completes la implementación inicial, prepara endpoints bien definidos, protección de rutas, carga/guardado en archivos `.json`, y asegura que todo funcione tanto online como en ejecución local.

Gracias, Copilot.
"""

# Comienza por definir la estructura inicial de Flask con los primeros endpoints y funciones clave.
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
import os
import json
import uuid
from datetime import datetime
import markdown2


# Clave secreta para dashboard admin
ADMIN_KEY = "123231"

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'partybin-secret')

# Carpeta de pastes
PASTES_DIR = os.path.join(os.path.dirname(__file__), 'data', 'pastes')
os.makedirs(PASTES_DIR, exist_ok=True)

def save_paste(data, paste_id):
	path = os.path.join(PASTES_DIR, f'{paste_id}.json')
	with open(path, 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=2)

def load_paste(paste_id):
	path = os.path.join(PASTES_DIR, f'{paste_id}.json')
	if not os.path.exists(path):
		return None
	with open(path, 'r', encoding='utf-8') as f:
		return json.load(f)

def list_pastes():
	files = [f for f in os.listdir(PASTES_DIR) if f.endswith('.json')]
	pastes = []
	for fname in files:
		with open(os.path.join(PASTES_DIR, fname), 'r', encoding='utf-8') as f:
			pastes.append(json.load(f))
	return sorted(pastes, key=lambda p: p.get('created_at', ''), reverse=True)

def generate_id():
	return uuid.uuid4().hex[:8]

@app.route('/')
def index():
	return render_template('create.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
	if request.method == 'POST':
		content = request.form.get('content', '').strip()
		custom_url = request.form.get('custom_url', '').strip()
		author = request.form.get('author', '').strip()
		protect = request.form.get('protect') == 'on'
		password = request.form.get('password', '').strip() if protect else ''
		tags = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
		paste_id = custom_url if custom_url else generate_id()
		if os.path.exists(os.path.join(PASTES_DIR, f'{paste_id}.json')):
			flash('La URL personalizada ya existe. Elige otra.', 'error')
			return render_template('create.html')
		html = markdown2.markdown(content, extras=["fenced-code-blocks", "tables", "strike", "task_list", "code-friendly"])
		paste = {
			'url': paste_id,
			'content': content,
			'html': html,
			'author': author,
			'protect': protect,
			'password': password,
			'tags': tags,
			'created_at': datetime.utcnow().isoformat(),
			'views': 0,
			'raw': content
		}
		save_paste(paste, paste_id)
		return redirect(url_for('view_paste', paste_id=paste_id))
	return render_template('create.html')

@app.route('/paste/<paste_id>')
def view_paste(paste_id):
	paste = load_paste(paste_id)
	if not paste:
		flash('Paste no encontrado.', 'error')
		return redirect(url_for('index'))
	# Si está protegido y es privado, requiere contraseña para ver
	if paste.get('protect', False):
		if request.method == 'POST':
			password = request.form.get('password', '')
			if password == paste.get('password', ''):
				paste['views'] += 1
				save_paste(paste, paste_id)
				return render_template('view.html', paste=paste)
			else:
				flash('Contraseña incorrecta.', 'error')
		return render_template('private.html')
	# No protegido
	paste['views'] += 1
	save_paste(paste, paste_id)
	return render_template('view.html', paste=paste)

@app.route('/paste/<paste_id>', methods=['POST'])
def view_paste_post(paste_id):
	return view_paste(paste_id)
@app.route('/edit/<paste_id>', methods=['GET', 'POST'])
def edit_paste(paste_id):
	paste = load_paste(paste_id)
	if not paste:
		flash('Paste no encontrado.', 'error')
		return redirect(url_for('index'))
	if request.method == 'POST':
		password = request.form.get('password', '')
		if paste.get('protect', False) and password != paste.get('password', ''):
			flash('Contraseña incorrecta.', 'error')
			return render_template('edit.html', paste=paste)
		content = request.form.get('content', '').strip()
		author = request.form.get('author', '').strip()
		tags = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
		html = markdown2.markdown(content, extras=["fenced-code-blocks", "tables", "strike", "task_list", "code-friendly"])
		paste['content'] = content
		paste['html'] = html
		paste['author'] = author
		paste['tags'] = tags
		paste['raw'] = content
		save_paste(paste, paste_id)
		flash('Paste actualizado.', 'success')
		return redirect(url_for('view_paste', paste_id=paste_id))
	return render_template('edit.html', paste=paste)
@app.route('/delete/<paste_id>')
def delete_paste(paste_id):
	admin = request.args.get('admin') == '1'
	if not admin:
		flash('Acceso denegado.', 'error')
		return redirect(url_for('index'))
	path = os.path.join(PASTES_DIR, f'{paste_id}.json')
	if os.path.exists(path):
		os.remove(path)
		flash('Paste eliminado.', 'success')
	else:
		flash('Paste no encontrado.', 'error')
	return redirect(url_for('dashboard'))
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	if request.method == 'POST':
		admin_key = request.form.get('admin_key', '')
		if admin_key == ADMIN_KEY:
			session['is_admin'] = True
			return redirect(url_for('dashboard'))
		else:
			flash('Clave admin incorrecta.', 'error')
			return render_template('dashboard.html', pastes=None)
	if session.get('is_admin'):
		pastes = list_pastes()
		return render_template('dashboard.html', pastes=pastes)
	return render_template('dashboard.html', pastes=None)

@app.route('/logout_admin')
def logout_admin():
	session.pop('is_admin', None)
	flash('Sesión admin cerrada.', 'success')
	return redirect(url_for('dashboard'))

@app.route('/export/<paste_id>')
def export_paste(paste_id):
	fmt = request.args.get('format', 'md')
	paste = load_paste(paste_id)
	if not paste:
		flash('Paste no encontrado.', 'error')
		return redirect(url_for('index'))
	filename = f'{paste_id}.{fmt}'
	if fmt == 'md':
		content = paste['content']
		mimetype = 'text/markdown'
	elif fmt == 'txt':
		content = paste['content']
		mimetype = 'text/plain'
	elif fmt == 'html':
		content = paste['html']
		mimetype = 'text/html'
	else:
		flash('Formato no soportado.', 'error')
		return redirect(url_for('view_paste', paste_id=paste_id))
	return app.response_class(content, mimetype=mimetype, headers={
		'Content-Disposition': f'attachment; filename={filename}'
	})

if __name__ == '__main__':
	app.run(debug=True)

