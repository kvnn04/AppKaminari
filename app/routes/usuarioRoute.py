from flask import Blueprint, render_template

usuario: Blueprint = Blueprint(name='usuario', import_name=__name__)

@usuario.route('/')
def usuarioPerfil():
    return render_template('usuarioPerfil.html')