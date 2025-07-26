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
# --- INICIO DE PARTYBIN ---
from flask import Flask, render_template, request, redirect, url_for, flash
import os

# Configuración básica
app = Flask(__name__)
app.secret_key = os.environ.get('PARTYBIN_SECRET', 'partybin_default_secret')

# Rutas principales
@app.route('/')
def index():
	return render_template('create.html')

@app.route('/create', methods=['GET', 'POST'])
def create_paste():
	if request.method == 'POST':
		# Aquí irá la lógica para crear el paste
		flash('Paste creado (demo)', 'success')
		return redirect(url_for('index'))
	return render_template('create.html')

@app.route('/view/<string:paste_url>')
def view_paste(paste_url):
	# Aquí irá la lógica para cargar y mostrar el paste
	return render_template('view.html', paste={})

@app.route('/edit/<string:paste_url>', methods=['GET', 'POST'])
def edit_paste(paste_url):
	# Aquí irá la lógica para editar el paste
	return render_template('edit.html', paste={})

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	# Aquí irá la lógica para mostrar el dashboard
	return render_template('dashboard.html', pastes=[])

# --- FIN DE PARTYBIN ---
# Arranque local
if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5000)

