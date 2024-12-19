from typing import List
from flask import Blueprint, redirect, render_template, session, url_for


carrito: Blueprint = Blueprint(name='carrito', import_name=__name__)


def inicializarCarrito():
    if 'carrito' not in session.keys():
        session['carrito'] = []
        session.modified = True



@carrito.route('/')
def carritoPage():

    inicializarCarrito()

    carritoSession = session.get('carrito', [])


    print(carritoSession)

    if carritoSession:
        totalPriceCarrito: float = 0
        cantidadItemCarrito: int = 0

        for i in carritoSession:

            totalPriceCarrito += i['totalPrecio']
            cantidadItemCarrito += 1

        return render_template('carrito.html', dataCarrito=carritoSession, cantidadItemCarrito=cantidadItemCarrito, totalPriceCarrito=totalPriceCarrito)
    
    return render_template('carrito.html')


@carrito.route('/<int:id>/<string:nombre>/<string:talle>/<string:color>/<int:cantidad>/<int:precio>')
def agregarProductoACarrito(id: int, nombre: str, talle: str, color: str, cantidad: int, precio: float):

    inicializarCarrito()

    totalPrecio = precio*cantidad

    dataProducto = { 'id': id,
        'nombre': nombre,
        'talle': talle,
        'cantidad': cantidad,
        'color': color,
        'precio': precio,
        'totalPrecio': totalPrecio
    }
    session['carrito'].append(dataProducto)
    session.modified = True


    print('hechoo, siuuuuu')
    return redirect(url_for('producto.productoPage', id=id, talleParams = talle, colorParams=color))
    

@carrito.route('/limpiar')
def limpiarCarrito():
    session['carrito'] = []
    session.modified = True
    return redirect(url_for('carrito.carritoPage'))

@carrito.route('/eliminar/<int:id>')
def eliminarProductoInCarrito(id: int):
    if session['carrito'] is None:
        return 'no existe carrito'
    
    listaProductosInCarrito = session['carrito']

    for producto in listaProductosInCarrito:
        if producto['id'] == id:
            session['carrito'].remove(producto)  # Elimina el diccionario de la lista
            session.modified = True  # Marca la sesión como modificada
            return redirect(url_for('carrito.carritoPage'))

    return redirect(url_for('home'))