from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Optional

class PasteForm(FlaskForm):
    title = StringField('Título', validators=[Optional()])
    content = TextAreaField('Contenido', validators=[DataRequired()])
    language = StringField('Lenguaje', validators=[Optional()])
    author = StringField('Firma/Alias', validators=[Optional()])
    tags = StringField('Etiquetas', validators=[Optional()])
    password = PasswordField('Contraseña', validators=[Optional()])
    edit_code = StringField('Código de edición', validators=[Optional()])
    max_views = IntegerField('Vistas máximas', validators=[Optional()])
    expires_at = DateTimeField('Expira en', validators=[Optional()])
    is_private = BooleanField('Paste privado')
    one_time = BooleanField('One-time view')
