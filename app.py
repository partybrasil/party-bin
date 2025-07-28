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

# Integración Flask + NiceGUI para PartyBin
from flask import Flask, request, redirect, url_for, send_file
from nicegui import ui
from models import Paste
import markdown2
import pygments
from pygments import lexers, formatters, highlight
from slugify import slugify
import os
import qrcode
from datetime import datetime

app = Flask(__name__)

PASTES_DIR = os.path.join(os.path.dirname(__file__), 'data', 'pastes')

# Utilidad para detectar lenguaje y resaltar código
def render_code_block(code, language=None):
	if not language:
		try:
			lexer = lexers.guess_lexer(code)
		except Exception:
			lexer = lexers.get_lexer_by_name('text')
	else:
		try:
			lexer = lexers.get_lexer_by_name(language)
		except Exception:
			lexer = lexers.get_lexer_by_name('text')
	formatter = formatters.HtmlFormatter(style='monokai', noclasses=False)
	return highlight(code, lexer, formatter)

# Rutas NiceGUI
@ui.page('/')
def index_page():
	ui.label('PartyBin - Pastebin Privado').classes('text-2xl font-bold')
	# Selector de tema visual
	import glob
	theme_files = glob.glob(os.path.join('static', 'themes', '*.css'))
	theme_names = [os.path.splitext(os.path.basename(f))[0] for f in theme_files if not f.endswith('monokai.css')]
	selected_theme = ui.select(theme_names, value='light').classes('w-32')
	theme_link = ui.html('<link id="theme-css" rel="stylesheet" href="/static/themes/light.css">')
	def change_theme(e):
		theme = selected_theme.value
		theme_link.content = f'<link id="theme-css" rel="stylesheet" href="/static/themes/{theme}.css">'
	selected_theme.on('update:model-value', change_theme)
	ui.button('Crear nuevo paste', on_click=lambda: ui.open('/create'))
	ui.button('Dashboard', on_click=lambda: ui.open('/dashboard'))
	ui.separator()
	pastes = Paste.all()
	for paste in pastes[-5:]:
		ui.link(paste.title or paste.id, f'/view/{paste.id}')

@ui.page('/create')
def create_page():
	ui.label('Crear nuevo paste').classes('text-xl font-bold')
	title = ui.input('Título')
	author = ui.input('Autor (opcional)')
	content = ui.textarea('Contenido', placeholder='Escribe tu texto, Markdown o código aquí...').classes('w-full h-40')
	language = ui.input('Lenguaje (opcional, autodetecta si vacío)')
	tags = ui.input('Tags (separados por coma)')
	password = ui.input('Contraseña (opcional)').props('type=password')
	private = ui.checkbox('Paste privado (solo por enlace)')
	max_views = ui.input('Máx. vistas (autodestrucción)').props('type=number')
	expire_at = ui.input('Expira en (YYYY-MM-DD HH:MM, opcional)')
	def save_paste():
		paste_id = slugify(title.value) if title.value else slugify(datetime.utcnow().isoformat())
		paste = Paste(
			id=paste_id,
			content=content.value,
			title=title.value,
			author=author.value,
			language=language.value,
			tags=[t.strip() for t in tags.value.split(',') if t.strip()],
			password=password.value if password.value else None,
			private=private.value,
			max_views=int(max_views.value) if max_views.value else None,
			expire_at=expire_at.value if expire_at.value else None
		)
		paste.save()
		ui.open(f'/view/{paste_id}')
	ui.button('Guardar', on_click=save_paste).classes('mt-4')

@ui.page('/view/{paste_id}')
def view_page(paste_id: str):
	paste = Paste.load(paste_id)
	if not paste:
		ui.label('Paste no encontrado').classes('text-red-500')
		return
	ui.label(paste.title or paste.id).classes('text-xl font-bold')
	ui.label(f'Autor: {paste.author}') if paste.author else None
	ui.label(f'Creado: {paste.created_at}')
	ui.label(f'Tags: {", ".join(paste.tags)}') if paste.tags else None
	ui.separator()
	# Renderizar contenido
	if paste.language:
		html = render_code_block(paste.content, paste.language)
		ui.html(html)
	else:
		# Markdown con bloques de código autodetectados
		html = markdown2.markdown(paste.content, extras=["fenced-code-blocks", "code-friendly"])
		ui.html(html)
	ui.button('Editar', on_click=lambda: ui.open(f'/edit/{paste.id}'))
	ui.button('Descargar .txt', on_click=lambda: send_file(os.path.join(PASTES_DIR, f'{paste.id}.json')))

@ui.page('/edit/{paste_id}')
def edit_page(paste_id: str):
	paste = Paste.load(paste_id)
	if not paste:
		ui.label('Paste no encontrado').classes('text-red-500')
		return
	ui.label(f'Editando: {paste.title or paste.id}').classes('text-xl font-bold')
	content = ui.textarea('Contenido', value=paste.content).classes('w-full h-40')
	def save_edit():
		paste.content = content.value
		paste.updated_at = datetime.utcnow().isoformat()
		paste.save()
		ui.open(f'/view/{paste.id}')
	ui.button('Guardar cambios', on_click=save_edit).classes('mt-4')

@ui.page('/dashboard')
def dashboard_page():
	ui.label('Dashboard de pastes recientes').classes('text-xl font-bold')
	pastes = Paste.all()
	for paste in pastes[-20:]:
		ui.link(paste.title or paste.id, f'/view/{paste.id}')

if __name__ == '__main__':
	ui.run()

