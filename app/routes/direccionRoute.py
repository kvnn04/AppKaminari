from flask import Blueprint, redirect, render_template, request, session, url_for, flash

from app.config.urlMiApi import BASE_URL
from app.logs.capturaDeError import logException
from app.src.forms.signUp import SignUpForm
from app.src.forms.direccion import DireccionUsuario
from app.src.token.auth import authenticate
from app.src.token.peticionesProtegidas import postRequest, protectedRequest
from pydantic import BaseModel, Field

direccionRoute = Blueprint('direccion', import_name=__name__)

def inicializarDireccionSession() -> None:
    if 'direccionUsuario' not in session.keys():
        session['direccionUsuario'] = []
        session.modified = True

@direccionRoute.route('/', methods=['GET', 'POST'])
def direccionUsuario():

    form = DireccionUsuario()

    if form.validate_on_submit():
        inicializarDireccionSession()
        provincia = form.provincia.data
        localidad = form.localidad.data
        calle = form.calle.data
        altura = form.altura.data
        departamento = form.departamento.data
        piso = form.piso.data
        codigoPostal = form.codigoPostal.data

        dataDireccion: dict[str, str|None] = {
            'provincia': provincia,
            'localidad' : localidad,
            'calle' : calle,
            'altura' : altura,
            'departamento' : departamento,
            'piso' : piso,
            'codigoPostal': codigoPostal
        }

        session['direccionUsuario'] = dataDireccion
        
        if 'urlPrevio' in session:
            urlProducto = session.pop('urlPrevio', url_for('home'))

            print(urlProducto)
            return redirect(urlProducto)


    return render_template('direccion.html', form=form)

@direccionRoute.route('/limpiar')
def limpiarDireccion():
    session['direccionUsuario'] = []
    session.modified = True
    return redirect(url_for('home'))