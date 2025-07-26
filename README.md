# 🥳 PartyBin - Tu Pastebin Privado y Potenciado en Flask

**PartyBin** es un clon completo y mejorado de [Rentry.co](https://rentry.co), desarrollado en **Python 3.10+** y **Flask**. Es una aplicación de tipo pastebin con Markdown enriquecido, soporte para código, autodestrucción inteligente, seguridad, firma, exportación y más. Ideal para uso personal o privado, y ejecutable tanto localmente como en la nube (Render.com).

---

## 🧱 Estructura del Proyecto

```
partybin/
│
├── app.py                  # App principal de Flask
├── requirements.txt        # Dependencias del proyecto
├── render.yaml             # Configuración de despliegue en Render
├── Procfile                # Definición de proceso para Gunicorn (Render)
├── .gitignore              # Archivos a ignorar por Git
├── README.md               # Este documento
│
├── templates/              # Archivos HTML Jinja2
│   ├── base.html
│   ├── create.html
│   ├── view.html
│   ├── edit.html
│   └── dashboard.html
│
├── static/                 # Archivos estáticos (CSS, JS, themes)
│   ├── style.css
│   ├── themes/
│   │   ├── light.css
│   │   ├── dark.css
│   │   └── hacker.css
│   └── js/
│       └── utils.js        # Copy-to-clipboard, contador, etc.
│
├── data/                   # Pastes almacenados (en JSON o SQLite)
│   ├── pastes/             # Un archivo JSON por paste
│   └── dashboard.json      # Datos locales del dashboard (modo local)
```

---

## 🧠 Funcionalidades Confirmadas

### Básicas (Clon de Rentry)

- Crear pastes anónimos
- Soporte completo de Markdown
- Preview en vivo
- URL personalizada o aleatoria
- Código de edición
- Eliminación o edición usando código
- Syntax highlighting por bloques de código
- Soporte para HTML crudo

### Avanzadas añadidas en PartyBin

- 🔐 Protección por contraseña (oculta todo el contenido hasta ingresar clave)
- 🔒 Protección de edición por código (estilo Rentry)
- ⏳ Autodestrucción por tiempo, fecha o vistas
- 🧠 Detección automática de lenguaje en bloques de código
- 🖼️ Vista previa automática de imágenes (links, base64, imgur)
- 🎨 Selector de tema (light / dark / hacker) con sistema modular
- ✍️ Firma opcional del autor (alias sin cuenta)
- 🧾 Vista raw y botón de copiar
- 📤 Exportación del paste (.txt, .md, .html)
- 📱 Generador de QR code para compartir
- 🏷️ Sistema de tags por paste
- 🗓️ Mostrar fecha de creación y último acceso
- ⏱️ Countdown visual hasta la expiración
- 🧩 Mini-dashboard local para gestión de tus pastes (offline)

---

## 🖥️ Uso Local

PartyBin puede ejecutarse **localmente** sin necesidad de conexión o despliegue. Al correr en modo local:

- Todos los pastes se guardan en `data/pastes/`
- El dashboard (`/dashboard`) muestra tus pastes creados
- Las funcionalidades funcionan sin modificar
- OBS: **funciona perfectamente en local**, pero los datos entre instancias (nube online y local) están **desacoplados**.

### 🚀 Instrucciones para uso local

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/partybin.git
cd partybin

# 2. Crea un entorno virtual (opcional pero recomendado)
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Ejecuta la app localmente
python app.py

# 5. Abre en tu navegador:
http://localhost:5000
```

---

## 🌍 Despliegue Online en Render

### 🔧 Requisitos

- Cuenta gratuita en [Render.com](https://render.com)
- Cuenta de GitHub con el repositorio `PartyBin` subido

### 🚀 Pasos para desplegar en Render

1. **Sube el proyecto a GitHub**
2. Entra en [Render &gt; Web Services &gt; New Web Service](https://dashboard.render.com)
3. Elige **"Deploy from a Git repository"**
4. Selecciona tu repo de PartyBin
5. Render detectará `requirements.txt` y `Procfile` automáticamente
6. Asegúrate que la línea de comando es:
   ```bash
   gunicorn app:app
   ```
7. Click en “Deploy Service”

Tu PartyBin estará disponible en una URL pública como:

```
https://partybin.onrender.com
```

---

## 🔐 Seguridad y Privacidad

- Cada paste puede tener:
  - **Código de edición** para cambiarlo o eliminarlo
  - **Contraseña de acceso completa** para proteger el contenido (checkbox)
- No requiere usuarios ni cuentas
- No guarda IPs ni cookies de rastreo

---

## 📦 Exportación

Cada paste se puede descargar o copiar como:

- `.txt`
- `.md`
- `.html`

---

## 🛠️ Dependencias Principales

```
Flask
markdown2
Pygments
python-slugify
qrcode
```

---

## 📂 Metadata soportada (en bloque Markdown inicial opcional)

```markdown
PAGE_TITLE = Mi título
PAGE_DESCRIPTION = Esto es una nota
OPTION_DISABLE_VIEWS = true
OPTION_DISABLE_SEARCH_ENGINE = true
OPTION_USE_ORIGINAL_PUB_DATE = true
ACCESS_RECOMMENDED_THEME = hacker
```

---

## 💡 Funciones Futuras (Backlog)

- Modo colaborativo (edición compartida)
- Shortlinks temporales
- Notificaciones Webhook al visualizar paste
- Soporte para archivos adjuntos (limitado)

---

## 🧙 Créditos

Proyecto creado por **Miguelinho** con ayuda de IA (ChatGPT + Copilot), como herramienta personal de pastes enriquecidos, segura, privada y extensible.

---

## 📜 Licencia

Este proyecto es de uso personal. Puedes adaptarlo, clonarlo o extenderlo libremente para uso educativo o privado. No para uso comercial sin permiso.

---
