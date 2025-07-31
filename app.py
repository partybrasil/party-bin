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


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from models import db
from routes.pastes import pastes_bp
from routes.dashboard import dashboard_bp
from routes.auth import auth_bp
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'partybin-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///partybin.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)

# Blueprints
app.register_blueprint(pastes_bp)
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def home():
	return render_template('home.html')

if __name__ == '__main__':
	app.run(debug=True)

