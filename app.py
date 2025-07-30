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


from flask import Flask
from config import Config
from models import db, bcrypt
from routes.pastes import pastes_bp
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(pastes_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

@app.before_request
def create_tables():
	if not hasattr(app, '_tables_created'):
		db.create_all()
		app._tables_created = True

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	print(f"\n * PartyBin corriendo en: http://127.0.0.1:{port} (o http://localhost:{port})\n   Presiona CTRL+C para detener el servidor.\n")
	app.run(debug=True, host='0.0.0.0', port=port)

