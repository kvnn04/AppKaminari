from typing import List
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class ProductFormColor(FlaskForm):
    color = SelectField('Color', validators=[DataRequired(message="Por favor, selecciona un color.")])
    submit = SubmitField('Seleccionar Color')

    def __init__(self, colorChoices: List[tuple], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color.choices = colorChoices


class ProductFormTalle(FlaskForm):
    talle = SelectField('Talle', validators=[DataRequired(message="Por favor, selecciona un talle.")])
    submit = SubmitField('Seleccionar Talle')

    def __init__(self, talleChoices: List[tuple], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.talle.choices = talleChoices

class FilterTalleByColor(FlaskForm):
    talle = SelectField('Talle', validators=[DataRequired(message="Por favor, selecciona un talle.")])
    color = SelectField('Color')
    submit = SubmitField('Comprar')

    def __init__(self, talleChoices: List[tuple], colorChoices: List[tuple], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.talle.choices = talleChoices
        self.color.choices = [("", "Selecciona un color (opcional)")] + colorChoices
