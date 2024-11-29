from flask import Blueprint, render_template

carrito: Blueprint = Blueprint(name='carrito', import_name=__name__)

@carrito.route('/')
def register():
    return render_template('carrito.html')