from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length
from app.src.forms.signUp import validatePasswordStrength

class SignInForm(FlaskForm):
    username: StringField = StringField(label='Email o username', validators=[DataRequired(message='Este campo es requrido'), Length(min=3, max=30)])
    pwd: PasswordField = PasswordField(
        label='Contraseña. EJ: Boka.1234',
        validators=[
            DataRequired(message='Este campo es obligatorio'),
            Length(min=8, max=1000, message='Debe tener al menos 8 caracteres.'),
            validatePasswordStrength
        ]
    )
    submit: SubmitField = SubmitField(label='Iniciar sesión')