from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

class SignInForm(FlaskForm):
    username: StringField = StringField(label='Username. EJ: kvnn_04')
    pwd: PasswordField = PasswordField(
        label='Contraseña. EJ: Boka.1234',
        validators=[
            DataRequired(message='Este campo es obligatorio'),
            Length(min=8, max=1000, message='Debe tener al menos 8 caracteres.')
        ]
    )
    submit: SubmitField = SubmitField(label='Iniciar sesión')