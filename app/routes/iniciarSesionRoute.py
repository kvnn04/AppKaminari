from flask import Blueprint, redirect, render_template, session,url_for, flash
from app.logs.capturaDeError import logException
from app.src.forms.signInForm import SignInForm
from app.src.token.auth import authenticate
from app.src.token.peticionesProtegidas import protectedRequest
from app.src.models.usuarioModels import Usuario

signIn: Blueprint = Blueprint(name='signIn', import_name=__name__)

@signIn.route('/', methods=['GET', 'POST'])
def iniciarSesion():
    formularioSignIn: SignInForm = SignInForm()
    if formularioSignIn.validate_on_submit():
        usuario: str|None =authenticate(formularioSignIn.username.data, formularioSignIn.pwd.data)
        if not usuario:
            error = 'Error al iniciar sesion'
            logException(exception=Exception(error))
            flash(message=error)
            return redirect(url_for('signIn.iniciarSesion'))
            # return render_template('signIn.html', form=formularioSignIn, error=error)
        dataUser: dict = protectedRequest('/usuario/getUsuario', method='get', token=usuario)
        if not dataUser['response']:
            logException(exception=Exception(dataUser['message']))
            error = 'Error al iniciar sesion'
            return render_template('signIn.html', form=formularioSignIn, error=error)
        print(dataUser)
        session['informationUsuario'] = dataUser['response']
        return redirect(url_for('home'))

    return render_template('signIn.html', form=formularioSignIn)