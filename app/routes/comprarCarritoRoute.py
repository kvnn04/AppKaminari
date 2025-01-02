# SDK de Mercado Pago
from typing import List
from flask import Blueprint, jsonify, redirect, request, url_for, session
from app.config.sdkMp import sdk
from app.logs.capturaDeError import logException
from app.src.token.peticionesProtegidas import getRequest

pagoCarritoRoute = Blueprint('pagoCarrito', import_name=__name__)

@pagoCarritoRoute.route('/', methods=['POST', 'GET'])
def pagoCarrito():

    '''
    Tiene que existir:
        -Usuario
        -DireccionUsuario
        -Productos
    Sino existe esto lo que va a ser es redireccionar a home

    PENDIENTE: tengo que avisarle al usuario, mostrar un tipo de mensaje
    '''

    productosInCarrito: List[dict]|None = session.get('carrito', [])


    if not productosInCarrito:
        return redirect(url_for('carrito.carritoPage'))
    
    user: dict[str,str] = session.get('informationUsuario', [])

    if not user:
        print(request.url)
        session['urlPrevio'] = request.url
        return redirect(url_for('signIn.iniciarSesion'))
    
    direccionUsuario: dict[str, str] = session.get('direccionUsuario', [])

    if not direccionUsuario:
        print(request.url)
        session['urlPrevio'] = request.url
        return redirect(url_for('direccion.direccionUsuario'))

    
    # idsProductosInCarrito = [id['id'] for id in productosInCarrito] # mio
    idsProductosInCarrito: List[int] = [id.get('id', None) for id in productosInCarrito if 'id' in id] # de la IA  

    productoPrecio: dict[str, str] = getRequest('/producto/getPriceByListIdProducto', params={'ids': idsProductosInCarrito})
    print(productoPrecio)
    productoPrecio: dict[str, int|str] = productoPrecio['response']

    preciosPorId: dict[str, int|float] = {item['id']: item['precio'] for item in productoPrecio}

    for item in productosInCarrito:
        if item['id'] in preciosPorId:
            item['precio'] = preciosPorId[item['id']]

    try:
        preference_data = {
            "items": [],
            "back_urls": {
                "success": url_for('pagoCarrito.paymentSuccessCarrito', _external=True),
                "failure": url_for('pagoCarrito.paymentFailedCarrito', _external=True),
                "pending": url_for('pagoCarrito.paymentPendingCarrito', _external=True)
            },
            "payer": {
                "name": user['nombre'],
                "email": user['email']
            },
            # "notification_url": "http://localhost:5000/pago/notificationss"
        }

        for i in productosInCarrito:
            data = {
                    "title": i['nombre'],
                    "quantity": float(i['precio']),
                    "currency_id": "ARS",  # Moneda
                    "unit_price": int(i['cantidad'])    # Precio unitario
                    }
            preference_data['items'].append(data)
        
        preference_response = sdk.preference().create(preference_data)
        preference_url = preference_response["response"]["init_point"]

    except Exception as e:
        logException(Exception)
        print(f"Error: {e}")
    return redirect(preference_url)


@pagoCarritoRoute.route('/paymentSuccess', methods=['GET'])
def paymentSuccessCarrito():
    # Aquí puedes capturar y procesar los datos que vienen por la URL
    payment_id = request.args.get('payment_id')  # Ejemplo: Obtener un parámetro llamado 'payment_id'
    status = request.args.get('status')         # Otro ejemplo: Obtener el estado del pago
    
    # Opcional: Guardar los datos en sesión o en una base de datos
    # if payment_id and status:
    #     session['payment_info'] = {
    #         'payment_id': payment_id,
    #         'status': status
    #     }
    #     print(session['payment_info'])

    session.permanent = True  # Refresca el tiempo de expiración cuando se accede

    
    if 'direccionUsuario' in session:
        session.pop('direccionUsuario')
        session.modified = True
        
    if 'carrito' in session:
        session.pop('carrito')
        session.modified = True

    return redirect(url_for('home'))

@pagoCarritoRoute.route('/paymentFailed', methods=['GET'])
def paymentFailedCarrito():
    direccionUsuario = session.get('direccionUsuario', [])
    if direccionUsuario:
        session['direccionUsuario'] = []
        session.modified = True
    return redirect(url_for('home'))

@pagoCarritoRoute.route('/paymentPending', methods=['GET'])
def paymentPendingCarrito():
    return redirect(url_for('home'))
    
