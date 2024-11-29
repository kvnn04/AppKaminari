from flask import Blueprint, redirect, render_template, flash, url_for

from app.logs.capturaDeError import logException
from app.src.token.peticionesProtegidas import getRequest

producto: Blueprint = Blueprint(name='producto', import_name=__name__)

@producto.route('/<int:id>')
def productoPage(id: int):
    respuesta = getRequest(endpoint="/producto/getProducto", params={'id': id})
    if respuesta['response'] is None:
        # error = 'no existe este producto'
        logException(exception=Exception(respuesta['message']))
        # flash(message=error)
        return redirect(url_for('home'))
    return render_template('producto.html', producto= respuesta['response'])