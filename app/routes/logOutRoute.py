from flask import Blueprint, redirect, session, url_for

logOut: Blueprint = Blueprint(name='logOut', import_name=__name__)

@logOut.route('/logout')
def logout():
    session.pop('informationUsuario', None)  # Elimina la clave específica
    return redirect(url_for('home'))