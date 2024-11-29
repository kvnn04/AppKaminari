from flask import Blueprint, redirect, render_template, session,url_for, flash
from app.logs.capturaDeError import logException
from app.src.forms.signInForm import SignInForm
from app.src.token.auth import authenticate
from app.src.token.peticionesProtegidas import protectedRequest

logOut: Blueprint = Blueprint(name='logOut', import_name=__name__)

@logOut.route('/logout')
def logout():
    session.pop('informationUsuario', None)  # Elimina la clave específica
    return redirect(url_for('home'))