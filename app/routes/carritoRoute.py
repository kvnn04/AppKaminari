from flask import Blueprint, redirect, render_template, session, url_for
from app.src.models.carritoModel import Carrito
from app.src.models.productoModel import Producto
carrito: Blueprint = Blueprint(name='carrito', import_name=__name__)


def inicializarCarrito():
    if 'carrito' not in session.keys():
        session['carrito'] = []
        session.modified = True



@carrito.route('/')
def carritoPage():

    inicializarCarrito()

    carritoSession = session.get('carrito', [])

    
    carritoBest: Carrito = Carrito()

    if carritoSession:

        for i in carritoSession:
            dataProducto: dict = i['data']
            producto: Producto = Producto(id=i['id'], nombre=dataProducto['nombre'], precio=dataProducto['precio'], talle=dataProducto['talle'])
            carritoBest.agregarProducto(producto=producto)
        
        print(carritoBest.producto)

        return render_template('carrito.html', dataCarrito=carritoSession)
    
    return render_template('carrito.html')


@carrito.route('/<int:id>/<string:nombre>/<string:talle>/<string:color>/<int:precio>')
def agregarProductoACarrito(id: int, nombre: str, talle: str, color: str, precio: int):

    inicializarCarrito()

    dataProducto = {'id': id, 'data' : {
        'nombre': nombre,
        'talle': talle,
        'color': color,
        'precio': precio
    }}



    # if 'carrito' not in session.keys():
    #     session['carrito'] = []

    session['carrito'].append(dataProducto)
    session.modified = True


    print('hechoo, siuuuuu')
    return redirect(url_for('producto.productoPage', id=id, talleParams = talle, colorParams=color))
    

@carrito.route('/limpiar')
def limpiarCarrito():
    session['carrito'] = []
    session.modified = True
    return redirect(url_for('carrito.carritoPage'))
