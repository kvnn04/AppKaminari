from flask import Blueprint, redirect, render_template, session,url_for, flash
from app.logs.capturaDeError import logException
from app.src.forms.signInForm import SignInForm
from app.src.token.auth import authenticate
from app.src.token.peticionesProtegidas import getRequest, postRequest, protectedRequest
from app.src.models.usuarioModels import Usuario

signIn: Blueprint = Blueprint(name='signIn', import_name=__name__)

@signIn.route('/', methods=['GET', 'POST'])
def iniciarSesion():
    formularioSignIn: SignInForm = SignInForm()
    
    if formularioSignIn.validate_on_submit():
        usuarioToken: str|None = authenticate(formularioSignIn.username.data, formularioSignIn.pwd.data) # con email
        if not usuarioToken:
            error = 'Error al iniciar sesion'
            logException(exception=Exception(error))
            flash(message=error)
            return redirect(url_for('signIn.iniciarSesion'))
        
        dataUser: dict = getRequest('/usuario/getUsuario', token=usuarioToken)
        if not dataUser['response']:
            logException(exception=Exception(dataUser['message']))
            error = 'Error al iniciar sesion'
            return render_template('signIn.html', form=formularioSignIn, error=error)
        print(dataUser)
        session['informationUsuario'] = dataUser['response']

        # print(session)

        if 'urlPrevio' in session:
            urlProducto = session.pop('urlPrevio', url_for('home'))
            session.modified = True
            return redirect(urlProducto)

        return redirect(url_for('home'))

    return render_template('signIn.html', form=formularioSignIn)