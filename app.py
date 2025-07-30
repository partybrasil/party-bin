# 👇 PROMPT MAESTRO PARA COPILOT – PARTY-BIN

"""
📌 CONTEXTO DEL PROYECTO:

Este repositorio contiene PARTY-BIN, una aplicación web desarrollada en Python con Flask, diseñada como un clon personalizado de Rentry.org, pero con muchas funciones avanzadas añadidas.

🧠 TU TAREA (GitHub Copilot + Visual Studio Code):

Lee cuidadosamente el archivo README.md de este repositorio.
A partir de la descripción completa allí incluida, **genera la estructura de carpetas, archivos y lógica necesaria** para que PARTY-BIN funcione exactamente como se especifica, sin añadir ni omitir funcionalidades.

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


import os
import json
import uuid
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort, session, make_response
from markdown2 import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
from pygments.formatters import HtmlFormatter
from slugify import slugify
import qrcode
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'partybin-secret')

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'pastes')
DASHBOARD_PATH = os.path.join(os.path.dirname(__file__), 'data', 'dashboard.json')
os.makedirs(DATA_DIR, exist_ok=True)

def load_paste(paste_id):
	path = os.path.join(DATA_DIR, f'{paste_id}.json')
	if not os.path.exists(path):
		return None
	with open(path, 'r', encoding='utf-8') as f:
		return json.load(f)

def save_paste(paste):
	path = os.path.join(DATA_DIR, f'{paste["url"]}.json')
	with open(path, 'w', encoding='utf-8') as f:
		json.dump(paste, f, ensure_ascii=False, indent=2)

def render_markdown(content, language=None):
	# Renderiza markdown y resalta bloques de código
	def codehilite(code, lang):
		try:
			lexer = get_lexer_by_name(lang) if lang else guess_lexer(code)
		except Exception:
			lexer = TextLexer()
		formatter = HtmlFormatter(nowrap=True)
		return highlight(code, lexer, formatter)
    
	import re
	def replacer(match):
		code = match.group(2)
		lang = match.group(1) or language
		return f'<pre class="code"><code>{codehilite(code, lang)}</code></pre>'
	# Reemplaza bloques de código markdown triple backtick
	content = re.sub(r'```([\w+-]*)\n([\s\S]*?)```', replacer, content)
	html = markdown(content, extras=["fenced-code-blocks", "tables", "strike", "cuddled-lists", "metadata"])
	# Vista previa automática de imágenes (imgur, base64, links directos)
	import re
	def img_replacer(match):
		url = match.group(1)
		if url.startswith('data:image') or url.startswith('http') or 'imgur.com' in url:
			return f'<img src="{url}" alt="image" />'
		return match.group(0)
	html = re.sub(r'!\[.*?\]\((.*?)\)', img_replacer, html)
	return html

def get_new_url(custom_url=None):
	if custom_url:
		url = slugify(custom_url)
	else:
		url = uuid.uuid4().hex[:8]
	# Asegura unicidad
	while os.path.exists(os.path.join(DATA_DIR, f'{url}.json')):
		url = uuid.uuid4().hex[:8]
	return url

def update_dashboard(paste):
	try:
		with open(DASHBOARD_PATH, 'r', encoding='utf-8') as f:
			data = json.load(f)
	except Exception:
		data = {"pastes": []}
	# Evita duplicados
	data["pastes"] = [p for p in data["pastes"] if p["url"] != paste["url"]]
	data["pastes"].insert(0, {"url": paste["url"], "title": paste.get("title"), "created": paste["created"]})
	with open(DASHBOARD_PATH, 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
	return redirect(url_for('create_paste'))

@app.route("/create", methods=["GET", "POST"])
def create_paste():
	if request.method == "POST":
		content = request.form["content"]
		title = request.form.get("title")
		language = request.form.get("language")
		custom_url = request.form.get("custom_url")
		password = request.form.get("password")
		author = request.form.get("author")
		tags = [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()]
		autodestruct = request.form.get("autodestruct", "none")
		privatize = request.form.get("privatize") == "on"
		url = get_new_url(custom_url)
		now = datetime.datetime.utcnow().isoformat()
		if password:
			paste = {
				"url": url,
				"title": title,
				"content": content,
				"language": language,
				"created": now,
				"updated": now,
				"views": 0,
				"author": author,
				"tags": tags,
				"autodestruct": autodestruct,
				"max_views": 1 if autodestruct == "one" else (None if autodestruct != "views" else 10),
				"password": generate_password_hash(password),
				"edit_code": None,
				"privatize": True,
			}
			flash("Paste privado creado. Usa la contraseña para ver y editar.", "success")
		elif privatize:
			# Si se marca privatizar pero no hay contraseña, se genera código de edición
			edit_code = uuid.uuid4().hex[:8]
			paste = {
				"url": url,
				"title": title,
				"content": content,
				"language": language,
				"created": now,
				"updated": now,
				"views": 0,
				"author": author,
				"tags": tags,
				"autodestruct": autodestruct,
				"max_views": 1 if autodestruct == "one" else (None if autodestruct != "views" else 10),
				"password": None,
				"edit_code": edit_code,
				"privatize": False,
			}
			flash(f"Paste protegido por código. Código de edición: {edit_code}", "success")
		else:
			# Público: cualquiera puede editar
			paste = {
				"url": url,
				"title": title,
				"content": content,
				"language": language,
				"created": now,
				"updated": now,
				"views": 0,
				"author": author,
				"tags": tags,
				"autodestruct": autodestruct,
				"max_views": 1 if autodestruct == "one" else (None if autodestruct != "views" else 10),
				"password": None,
				"edit_code": None,
				"privatize": False,
			}
			flash("Paste público creado. Cualquiera puede editarlo.", "success")
		save_paste(paste)
		update_dashboard(paste)
		return redirect(url_for('view_paste', paste_id=url))
	return render_template("create.html")

@app.route("/view/<paste_id>", methods=["GET"])
def view_paste(paste_id):
	paste = load_paste(paste_id)
	if not paste:
		abort(404)
	# Si requiere contraseña y no está autenticado, no mostrar contenido (el modal JS lo pedirá)
	show_content = True
	if paste.get("privatize") and paste.get("password"):
		if not session.get(f"auth_{paste_id}"):
			show_content = False
	# Autodestrucción por vistas (solo si se puede ver)
	if show_content:
		paste["views"] = paste.get("views", 0) + 1
		if paste.get("autodestruct") == "views" and paste.get("max_views") and paste["views"] >= int(paste["max_views"]):
			os.remove(os.path.join(DATA_DIR, f'{paste_id}.json'))
			flash("Este paste se ha autodestruido por límite de vistas.", "info")
			return redirect(url_for('index'))
		save_paste(paste)
		html = render_markdown(paste["content"], paste.get("language"))
		paste["html"] = html
	else:
		paste["html"] = "<div style='text-align:center;color:#888;font-size:1.2em;margin:2em 0;'>🔒 Este paste está protegido por contraseña.</div>"
	return render_template("view.html", paste=paste, show_content=show_content)

@app.route("/auth/<paste_id>", methods=["POST"])
def auth_paste(paste_id):
	paste = load_paste(paste_id)
	if not paste or not paste.get("password"):
		abort(404)
	password = None
	if request.is_json:
		data = request.get_json(silent=True)
		if data:
			password = data.get("password")
	if not password:
		password = request.form.get("password")
	if check_password_hash(paste["password"], password):
		session[f"auth_{paste_id}"] = True
		# AJAX: Si es petición JS, responde JSON
		if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			return {"success": True}
		return redirect(url_for('view_paste', paste_id=paste_id, auth=1))
	# AJAX: Si es petición JS, responde JSON
	if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		return {"success": False, "error": "Contraseña incorrecta"}, 401
	flash("Contraseña incorrecta", "danger")
	return redirect(url_for('view_paste', paste_id=paste_id))

@app.route("/edit/<paste_id>", methods=["GET", "POST"])
def edit_paste(paste_id):
	paste = load_paste(paste_id)
	if not paste:
		abort(404)
	# Si tiene contraseña, requiere autenticación de sesión
	if paste.get("password"):
		if not session.get(f"auth_{paste_id}"):
			return render_template("edit.html", paste=None, need_password=True, paste_id=paste_id)
	# Si tiene código de edición, pedirlo
	elif paste.get("edit_code"):
		code = request.args.get("code") or request.form.get("code")
		if not code or code != paste.get("edit_code"):
			return '''<form method="post"><input type="text" name="code" placeholder="Código de edición"><button type="submit">Entrar</button></form>'''
	# Si es público, cualquiera puede editar
	if request.method == "POST":
		paste["content"] = request.form["content"]
		paste["title"] = request.form.get("title")
		paste["language"] = request.form.get("language")
		paste["author"] = request.form.get("author")
		paste["tags"] = [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()]
		# Privatización y contraseña reversibles
		password = request.form.get("password")
		privatize = request.form.get("privatize") == "on"
		if password:
			paste["password"] = generate_password_hash(password)
			paste["edit_code"] = None
			paste["privatize"] = True
		elif privatize:
			if not paste.get("edit_code"):
				paste["edit_code"] = uuid.uuid4().hex[:8]
			paste["password"] = None
			paste["privatize"] = False
		else:
			paste["password"] = None
			paste["edit_code"] = None
			paste["privatize"] = False
		paste["updated"] = datetime.datetime.utcnow().isoformat()
		save_paste(paste)
		flash("Paste actualizado", "success")
		return redirect(url_for('view_paste', paste_id=paste_id))
	return render_template("edit.html", paste=paste, need_password=False, paste_id=paste_id)

@app.route("/delete/<paste_id>", methods=["POST"])
def delete_paste(paste_id):
	paste = load_paste(paste_id)
	if not paste:
		abort(404)
	code = request.form.get("code")
	if not code or code != paste.get("edit_code"):
		return {"success": False, "error": "Código de edición incorrecto"}, 401
	os.remove(os.path.join(DATA_DIR, f'{paste_id}.json'))
	# Quitar del dashboard
	try:
		with open(DASHBOARD_PATH, 'r', encoding='utf-8') as f:
			data = json.load(f)
		data["pastes"] = [p for p in data["pastes"] if p["url"] != paste_id]
		with open(DASHBOARD_PATH, 'w', encoding='utf-8') as f:
			json.dump(data, f, ensure_ascii=False, indent=2)
	except Exception:
		pass
	flash("Paste eliminado", "success")
	return {"success": True}
@app.route("/qr/<paste_id>")
def qr_paste(paste_id):
	import io
	paste = load_paste(paste_id)
	if not paste:
		abort(404)
	if paste.get("privatize") and paste.get("password") and not session.get(f"auth_{paste_id}"):
		abort(403)
	url = request.url_root.rstrip('/') + url_for('view_paste', paste_id=paste_id)
	img = qrcode.make(url)
	buf = io.BytesIO()
	img.save(buf, format='PNG')
	buf.seek(0)
	return send_file(buf, mimetype='image/png')

@app.route("/preview", methods=["POST"])
def preview():
	data = request.get_json()
	content = data.get('content', '')
	html = render_markdown(content)
	return html
	if request.method == "POST" and request.form.get("content"):
		paste["content"] = request.form["content"]
		paste["title"] = request.form.get("title")
		paste["language"] = request.form.get("language")
		paste["author"] = request.form.get("author")
		paste["tags"] = [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()]
		paste["updated"] = datetime.datetime.utcnow().isoformat()
		save_paste(paste)
		flash("Paste actualizado", "success")
		return redirect(url_for('view_paste', paste_id=paste_id))
	return render_template("edit.html", paste=paste)

@app.route("/raw/<paste_id>")
def raw_paste(paste_id):
	paste = load_paste(paste_id)
	if not paste:
		abort(404)
	if paste.get("privatize") and paste.get("password") and not session.get(f"auth_{paste_id}"):
		abort(403)
	return paste["content"], 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.route("/export/<paste_id>")
def export_paste(paste_id):
	fmt = request.args.get("fmt", "txt")
	paste = load_paste(paste_id)
	if not paste:
		abort(404)
	if paste.get("privatize") and paste.get("password") and not session.get(f"auth_{paste_id}"):
		abort(403)
	filename = f"{paste_id}.{fmt}"
	if fmt == "txt":
		content = paste["content"]
		mimetype = "text/plain"
	elif fmt == "md":
		content = paste["content"]
		mimetype = "text/markdown"
	elif fmt == "html":
		content = render_markdown(paste["content"], paste.get("language"))
		mimetype = "text/html"
	else:
		abort(400)
	return content, 200, {"Content-Type": mimetype, "Content-Disposition": f"attachment; filename={filename}"}

@app.route("/dashboard")
def dashboard():
	try:
		with open(DASHBOARD_PATH, 'r', encoding='utf-8') as f:
			data = json.load(f)
	except Exception:
		data = {"pastes": []}
	return render_template("dashboard.html", pastes=data["pastes"])

if __name__ == "__main__":
	app.run(debug=True)

