from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, EmailField, SubmitField, PasswordField, ValidationError,IntegerField
from wtforms.validators import DataRequired, EqualTo, Length,NumberRange, Optional

# def validatePasswordStrength(form, field):
#     """
#     Valida que la contraseña cumpla con requisitos de seguridad:
#     - Al menos un número
#     - Al menos una letra mayúscula
#     - Al menos un carácter especial
#     """
#     password = field.data
#     if not any(char.isdigit() for char in password):
#         raise ValidationError('La contraseña debe contener al menos un número.')
#     if not any(char.isupper() for char in password):
#         raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
#     if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/`~" for char in password):
#         raise ValidationError('La contraseña debe contener al menos un carácter especial.')

def validarLongitudAltura(form, field):
    value = str(field.data)
    if len(value) < 1:
        raise ValidationError('El código postal debe tener al menos 5 dígitos.')
    if len(value) > 8:
        raise ValidationError('El código postal no debe tener más de 8 dígitos.')
provincias = [
        "Ciudad Autónoma de Buenos Aires",
        "Buenos Aires",
        "Catamarca",
        "Chaco",
        "Chubut",
        "Córdoba",
        "Corrientes",
        "Entre Ríos",
        "Formosa",
        "Jujuy",
        "La Pampa",
        "La Rioja",
        "Mendoza",
        "Misiones",
        "Neuquén",
        "Río Negro",
        "Salta",
        "San Juan",
        "San Luis",
        "Santa Cruz",
        "Santa Fe",
        "Santiago del Estero",
        "Tierra del Fuego",
        "Tucumán"
        ]

provincias.sort()

class DireccionUsuario(FlaskForm):
    provincia = SelectField(label='Provincia', choices=[(provincia, provincia) for provincia in provincias], validators=[DataRequired(message='Este campo es requerido')])
    localidad: StringField = StringField(label='Localidad', validators=[DataRequired(message='Este campo es requrido'), Length(min=2, max=20)])
    calle: StringField = StringField(label='Calle', validators=[DataRequired(message='Este campo es requrido'), Length(min=3, max=20)])
    altura: StringField = StringField(label='Altura', validators=[DataRequired(message='Este campo es requrido'), validarLongitudAltura])
    piso: StringField = StringField(label='Piso', validators=[Length(min=1, max=100), Optional()])
    departamento: StringField = StringField(label='Departamento', validators=[Length(max=20), Optional()]) 
    codigoPostal: StringField = StringField(label='Código postal', validators=[DataRequired(message='Este campo es requerido'), Length(min=3, max=10)])

    submit: SubmitField = SubmitField('Enviar')