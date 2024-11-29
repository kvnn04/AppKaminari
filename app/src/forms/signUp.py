from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length

def validatePasswordStrength(form, field):
    """
    Valida que la contraseña cumpla con requisitos de seguridad:
    - Al menos un número
    - Al menos una letra mayúscula
    - Al menos un carácter especial
    """
    password = field.data
    if not any(char.isdigit() for char in password):
        raise ValidationError('La contraseña debe contener al menos un número.')
    if not any(char.isupper() for char in password):
        raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
    if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/`~" for char in password):
        raise ValidationError('La contraseña debe contener al menos un carácter especial.')

class SignUpForm(FlaskForm):
    nombre: StringField = StringField(label='Nombre')
    apellido: StringField = StringField(label='Apellido')
    email: EmailField = EmailField(label='email@gmail.com')
    username: StringField = StringField(label='username', validators=[DataRequired(message='Este campo es requerido ')])
    pwd: PasswordField = PasswordField(
        label='Contraseña.1234',
        validators=[
            DataRequired(message='Este campo es obligatorio'),
            Length(min=8, max=1000, message='Debe tener al menos 8 caracteres.'),
            validatePasswordStrength
        ]
    )
    pwdVerify: PasswordField = PasswordField(
        label='Repetir contraseña',
        validators=[
            DataRequired(message='Este campo es obligatorio'),
            EqualTo('pwd', message='Las contraseñas deben coincidir.')
        ]
    )
    submit: SubmitField = SubmitField(label='Registrarme')