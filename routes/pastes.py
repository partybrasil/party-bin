

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from models import db, Paste
from utils import generate_url, highlight_code
from datetime import datetime, timedelta
import qrcode
import io

pastes_bp = Blueprint('pastes', __name__)

# Generar QR para compartir
@pastes_bp.route('/qr/<string:url>')
def qr_code(url):
    paste_url = request.url_root.rstrip('/') + '/' + url
    img = qrcode.make(paste_url)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

# Filtrar por tags
@pastes_bp.route('/tag/<string:tag>')
def pastes_by_tag(tag):
    pastes = Paste.query.filter(Paste.tags.like(f'%{tag}%')).order_by(Paste.created_at.desc()).all()
    return render_template('dashboard.html', pastes=pastes, tag=tag)

@pastes_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        language = request.form.get('language') or None
        url_custom = request.form.get('url')
        tags = request.form.get('tags')
        author = request.form.get('author')
        password = request.form.get('password')
        edit_code = request.form.get('edit_code')
        max_views = request.form.get('max_views')
        expires_at = request.form.get('expires_at')
        one_time = True if request.form.get('one_time') else False
        is_private = True if request.form.get('is_private') else False

        # Validaciones y advertencias
        if is_private and not password:
            flash('Para hacer el paste privado debes definir una contraseña.', 'error')
            return render_template('index.html')
        if password and not is_private:
            flash('Advertencia: El paste será público aunque tenga contraseña, a menos que marques "Paste privado".', 'warning')

        # Generar URL
        url = url_custom.strip() if url_custom else generate_url()
        if Paste.query.filter_by(url=url).first():
            flash('La URL personalizada ya existe, elige otra.', 'error')
            return render_template('index.html')

        # Procesar expiración
        expires_dt = None
        if expires_at:
            try:
                expires_dt = datetime.strptime(expires_at, '%Y-%m-%dT%H:%M')
            except Exception:
                flash('Formato de fecha de expiración inválido.', 'error')
                return render_template('index.html')

        # Procesar max_views
        try:
            max_views = int(max_views) if max_views else None
        except Exception:
            flash('El número de vistas máximas debe ser un número.', 'error')
            return render_template('index.html')

        # Hash de contraseña si aplica
        paste = Paste(
            url=url,
            title=title,
            content=content,
            language=language,
            tags=tags,
            author=author,
            edit_code=edit_code,
            max_views=max_views,
            expires_at=expires_dt,
            one_time=one_time,
            is_private=is_private
        )
        if password:
            paste.set_password(password)

        db.session.add(paste)
        db.session.commit()
        flash('¡Paste creado exitosamente!', 'success')
        return redirect(url_for('pastes.view_paste', url=url))
    return render_template('index.html')


@pastes_bp.route('/<string:url>', methods=['GET', 'POST'])
def view_paste(url):
    paste = Paste.query.filter_by(url=url).first_or_404()

    # Expiración por tiempo
    if paste.expires_at and datetime.utcnow() > paste.expires_at:
        db.session.delete(paste)
        db.session.commit()
        flash('Este paste ha expirado.', 'error')
        return redirect(url_for('pastes.index'))

    # Expiración por vistas
    if paste.max_views is not None and paste.views >= paste.max_views:
        db.session.delete(paste)
        db.session.commit()
        flash('Este paste ha alcanzado el límite de vistas.', 'error')
        return redirect(url_for('pastes.index'))

    # Protección privada
    if paste.is_private:
        if request.method == 'POST':
            password = request.form.get('password')
            if not password or not paste.check_password(password):
                flash('Contraseña incorrecta.', 'error')
                return render_template('paste.html', paste=None, require_password=True, url=url)
            session[f'paste_access_{url}'] = True
        elif not session.get(f'paste_access_{url}'):
            return render_template('paste.html', paste=None, require_password=True, url=url)

    # Incrementar vistas
    paste.views += 1
    paste.last_viewed = datetime.utcnow()
    db.session.commit()

    # Autodestrucción one-time
    if paste.one_time:
        db.session.delete(paste)
        db.session.commit()
        flash('Este paste era de un solo uso y ha sido destruido.', 'info')
        return redirect(url_for('pastes.index'))

    # Resaltado de sintaxis
    content_html = highlight_code(paste.content, paste.language)
    paste.content = content_html

    return render_template('paste.html', paste=paste, require_password=False, url=url)

# Edición de pastes
@pastes_bp.route('/edit/<string:url>', methods=['GET', 'POST'])
def edit_paste(url):
    paste = Paste.query.filter_by(url=url).first_or_404()
    if request.method == 'POST':
        edit_code = request.form.get('edit_code')
        password = request.form.get('password')
        # Verificación de código de edición o contraseña
        if paste.edit_code and edit_code != paste.edit_code:
            flash('Código de edición incorrecto.', 'error')
            return render_template('edit.html', paste=paste)
        if paste.is_private and not paste.check_password(password):
            flash('Contraseña incorrecta.', 'error')
            return render_template('edit.html', paste=paste)
        # Actualizar campos
        paste.title = request.form.get('title')
        paste.content = request.form.get('content')
        paste.language = request.form.get('language')
        paste.tags = request.form.get('tags')
        paste.author = request.form.get('author')
        db.session.commit()
        flash('Paste actualizado.', 'success')
        return redirect(url_for('pastes.view_paste', url=url))
    return render_template('edit.html', paste=paste)

# Exportar raw
@pastes_bp.route('/raw/<string:url>')
def raw_paste(url):
    paste = Paste.query.filter_by(url=url).first_or_404()
    return paste.content, 200, {'Content-Type': 'text/plain; charset=utf-8'}

# Exportar .txt
@pastes_bp.route('/export/txt/<string:url>')
def export_txt(url):
    paste = Paste.query.filter_by(url=url).first_or_404()
    return paste.content, 200, {
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Disposition': f'attachment; filename="{url}.txt"'
    }

# Exportar .md
@pastes_bp.route('/export/md/<string:url>')
def export_md(url):
    paste = Paste.query.filter_by(url=url).first_or_404()
    return paste.content, 200, {
        'Content-Type': 'text/markdown; charset=utf-8',
        'Content-Disposition': f'attachment; filename="{url}.md"'
    }

# Exportar .html
@pastes_bp.route('/export/html/<string:url>')
def export_html(url):
    paste = Paste.query.filter_by(url=url).first_or_404()
    content_html = highlight_code(paste.content, paste.language)
    html = f"<html><body>{content_html}</body></html>"
    return html, 200, {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Disposition': f'attachment; filename="{url}.html"'
    }

# Dashboard básico (requiere clave secreta por POST)
@pastes_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    pastes = None
    if request.method == 'POST':
        secret = request.form.get('secret')
        # Clave secreta simple, puedes mejorar esto
        if secret == 'partybin-secret':
            pastes = Paste.query.order_by(Paste.created_at.desc()).limit(50).all()
        else:
            flash('Clave secreta incorrecta.', 'error')
    return render_template('dashboard.html', pastes=pastes)
