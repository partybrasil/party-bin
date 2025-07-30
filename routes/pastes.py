
import io
import base64
import qrcode
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Paste
import markdown2
import pygments
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
from datetime import datetime
import os

pastes_bp = Blueprint('pastes', __name__)

@pastes_bp.route('/raw/<url_id>')
def raw_paste(url_id):
    paste = Paste.load(url_id)
    if not paste:
        flash('Paste no encontrado.', 'danger')
        return redirect(url_for('index'))
    return render_template('raw.html', paste=paste)

@pastes_bp.route('/export/<url_id>')
def export_paste(url_id):
    fmt = request.args.get('fmt', 'txt')
    paste = Paste.load(url_id)
    if not paste:
        flash('Paste no encontrado.', 'danger')
        return redirect(url_for('index'))
    filename = f"{paste.title or paste.url_id}.{fmt}"
    content = paste.content
    if fmt == 'md':
        content = paste.content
        mimetype = 'text/markdown'
    elif fmt == 'html':
        content = f"<pre>{paste.content}</pre>"
        mimetype = 'text/html'
    else:
        mimetype = 'text/plain'
    return (content, 200, {
        'Content-Type': mimetype + '; charset=utf-8',
        'Content-Disposition': f'attachment; filename="{filename}"'
    })

@pastes_bp.route('/qr/<url_id>')
def qr_paste(url_id):
    paste = Paste.load(url_id)
    if not paste:
        flash('Paste no encontrado.', 'danger')
        return redirect(url_for('index'))
    url = url_for('pastes.view_paste', url_id=paste.url_id, _external=True)
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    qr_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return render_template('qr.html', paste=paste, qr_base64=qr_base64)

pastes_bp = Blueprint('pastes', __name__)

@pastes_bp.route('/new', methods=['GET', 'POST'])
def new_paste():
    if request.method == 'POST':
        content = request.form.get('content', '')
        title = request.form.get('title', '')
        lang = request.form.get('lang', '')
        author = request.form.get('author', '')
        theme = request.form.get('theme', 'light')
        tags = request.form.get('tags', '').split(',') if request.form.get('tags') else []
        private = bool(request.form.get('private'))
        public = bool(request.form.get('public'))
        password = request.form.get('password') or None
        url_id = request.form.get('url_id') or None
        # Validaciones de privatización y público
        if private and not password:
            flash('Debes definir una contraseña para privatizar el paste.', 'warning')
            return render_template('new.html')
        if public and password:
            flash('Un paste público no debe tener contraseña. Elimínala para continuar.', 'warning')
            return render_template('new.html')
        # Validar url_id si se define
        if url_id:
            import re
            if not re.match(r'^[a-zA-Z0-9_-]+$', url_id):
                flash('La URL personalizada solo puede contener letras, números, guiones y guiones bajos.', 'danger')
                return render_template('new.html')
            # Verificar si ya existe
            from models import Paste
            if Paste.load(url_id):
                flash('La URL personalizada ya está en uso.', 'danger')
                return render_template('new.html')
        paste = Paste(content=content, title=title, lang=lang, author=author, tags=tags, theme=theme, private=private, public=public, password=password, url_id=url_id)
        paste.save()
        flash('Paste creado correctamente!', 'success')
        return redirect(url_for('pastes.view_paste', url_id=paste.url_id))
    return render_template('new.html')

@pastes_bp.route('/<url_id>')
def view_paste(url_id):
    paste = Paste.load(url_id)
    if not paste:
        flash('Paste no encontrado.', 'danger')
        return redirect(url_for('index'))
    # Protección por contraseña para visualizar
    if paste.private and not session.get(f'auth_{paste.url_id}'):
        if request.method == 'POST':
            password = request.form.get('password')
            if password and paste.password and password == paste.password:
                session[f'auth_{paste.url_id}'] = True
                return redirect(url_for('pastes.view_paste', url_id=paste.url_id))
            else:
                flash('Contraseña incorrecta.', 'danger')
        return render_template('password_prompt.html', url_id=paste.url_id)
    # Detección de lenguaje
    code = paste.content
    lang = paste.lang
    lexer = None
    if lang:
        try:
            lexer = get_lexer_by_name(lang)
        except Exception:
            lexer = None
    if not lexer:
        try:
            lexer = guess_lexer(code)
        except Exception:
            lexer = TextLexer()
    formatter = HtmlFormatter(linenos=True, cssclass="codehilite")
    highlighted = highlight(code, lexer, formatter)
    return render_template('paste.html', paste=paste, highlighted=highlighted, css=formatter.get_style_defs('.codehilite'))
@pastes_bp.route('/edit/<url_id>', methods=['GET', 'POST'])
def edit_paste(url_id):
    paste = Paste.load(url_id)
    if not paste:
        flash('Paste no encontrado.', 'danger')
        return redirect(url_for('index'))
    # Protección por contraseña para editar
    if paste.private and not session.get(f'auth_{paste.url_id}_edit'):
        if request.method == 'POST' and 'password' in request.form:
            password = request.form.get('password')
            if password and paste.password and password == paste.password:
                session[f'auth_{paste.url_id}_edit'] = True
                return redirect(url_for('pastes.edit_paste', url_id=paste.url_id))
            else:
                flash('Contraseña incorrecta.', 'danger')
        return render_template('password_prompt.html', url_id=paste.url_id, edit=True)
    # Solo procesar edición si el usuario ya está autenticado y el formulario es de edición
    if request.method == 'POST' and 'title' in request.form and 'content' in request.form:
        # Guardar versión anterior
        import json, datetime
        version_dir = os.path.join(os.path.dirname(paste.filepath), 'versions')
        os.makedirs(version_dir, exist_ok=True)
        version_file = os.path.join(version_dir, f'{paste.url_id}_{datetime.datetime.utcnow().isoformat().replace(":", "-")}.json')
        with open(version_file, 'w', encoding='utf-8') as vf:
            json.dump(paste.__dict__, vf, ensure_ascii=False, indent=2)
        # Actualizar paste
        paste.title = request.form.get('title', '')
        paste.content = request.form.get('content', '')
        paste.lang = request.form.get('lang', '')
        paste.tags = request.form.get('tags', '').split(',') if request.form.get('tags') else []
        paste.author = request.form.get('author', '')
        paste.private = bool(request.form.get('private'))
        paste.public = bool(request.form.get('public'))
        password = request.form.get('password') or None
        # Validaciones de privatización y público
        if paste.private and not password and not paste.password:
            flash('Debes definir una contraseña para privatizar el paste.', 'warning')
            return render_template('edit.html', paste=paste)
        if paste.public and (password or paste.password):
            flash('Un paste público no debe tener contraseña. Elimínala para continuar.', 'warning')
            return render_template('edit.html', paste=paste)
        paste.password = password
        paste.save()
        flash('Paste actualizado correctamente!', 'success')
        return redirect(url_for('pastes.view_paste', url_id=paste.url_id))
    return render_template('edit.html', paste=paste)
@pastes_bp.route('/delete/<url_id>', methods=['GET'])
def delete_paste(url_id):
    paste = Paste.load(url_id)
    if not paste:
        flash('Paste no encontrado.', 'danger')
        return redirect(url_for('pastes.dashboard'))
    try:
        os.remove(paste.filepath)
        flash('Paste eliminado correctamente.', 'success')
    except Exception:
        flash('No se pudo eliminar el paste.', 'danger')
    return redirect(url_for('pastes.dashboard'))
@pastes_bp.route('/dashboard', methods=['GET'])
def dashboard():
    # Clave secreta simple por query param para acceso (mejorar a futuro)
    secret = request.args.get('key')
    # TODO: Mejorar seguridad, por ahora acceso libre
    q = request.args.get('q', '').lower()
    pastes = Paste.list_all()
    if q:
        pastes = [p for p in pastes if q in p.title.lower() or q in p.content.lower() or any(q in t.lower() for t in p.tags)]
    return render_template('dashboard.html', pastes=pastes)
@pastes_bp.route('/password/<url_id>', methods=['GET', 'POST'])
def password_prompt(url_id):
    edit = request.args.get('edit', False)
    if request.method == 'POST':
        password = request.form.get('password')
        paste = Paste.load(url_id)
        if paste and password and paste.password and password == paste.password:
            if edit:
                session[f'auth_{paste.url_id}_edit'] = True
            else:
                session[f'auth_{paste.url_id}'] = True
            return redirect(url_for('pastes.edit_paste' if edit else 'pastes.view_paste', url_id=url_id))
        else:
            flash('Contraseña incorrecta.', 'danger')
    return render_template('password_prompt.html', url_id=url_id, edit=edit)
