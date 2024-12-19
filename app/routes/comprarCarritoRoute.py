# SDK de Mercado Pago
from flask import Blueprint, jsonify, redirect, request, url_for, session
from app.config.sdkMp import sdk
from app.logs.capturaDeError import logException
from app.src.token.peticionesProtegidas import getRequest

pagoCarritoRoute = Blueprint('pagoCarrito', import_name=__name__)

@pagoCarritoRoute.route('/', methods=['POST', 'GET'])
def pagoCarrito():

    productosInCarrito = session.get('carrito', [])

    if not productosInCarrito:
        return redirect(url_for('home'))
    
    user = session.get('informationUsuario', [])
    if not user:
        print(user)
        return redirect(url_for('home'))
    
    # idsProductosInCarrito = [id['id'] for id in productosInCarrito] # mio
    idsProductosInCarrito = [id.get('id', None) for id in productosInCarrito if 'id' in id] # de la IA

    productoPrecio = getRequest('/producto/getPriceByListIdProducto', params={'ids': idsProductosInCarrito})
    
    if not user:
        print(user)
        return redirect(url_for('home'))
    
    productoPrecio = productoPrecio['response']

    preciosPorId = {item['id']: item['precio'] for item in productoPrecio}

    for item in productosInCarrito:
        if item['id'] in preciosPorId:
            item['precio'] = preciosPorId[item['id']]

    try:
        preference_data = {
            "items": [],
            "back_urls": {
                "success": url_for('pagoCarrito.paymentSuccessCarrito', _external=True),
                "failure": url_for('pago.Carrito.paymentFailedCarrito', _external=True),
                "pending": url_for('pagoCarrito.paymentPendingCarrito', _external=True)
            },

            # "external_reference": "ORDEN12345",  # Puedes cambiarlo por un ID único generado por tu sistema
            "payer": {
                "name": user['nombre'],
                "email": user['email']
            },
            # "notification_url": "http://localhost:5000/pago/notificationss"
        }

        for i in productosInCarrito:
            data = {
                    "title": i['nombre'],
                    "quantity": i['precio'],
                    "currency_id": "ARS",  # Moneda
                    "unit_price": i['cantidad']    # Precio unitario
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
    if payment_id and status:
        session['payment_info'] = {
            'payment_id': payment_id,
            'status': status
        }
        print(session['payment_info'])
    
    # Redirige a 'home' sin los datos adicionales en la URL
    return redirect(url_for('home'))

@pagoCarritoRoute.route('/paymentFailed', methods=['GET'])
def paymentFailedCarrito():
    return redirect(url_for('home'))

@pagoCarritoRoute.route('/paymentPending', methods=['GET'])
def paymentPendingCarrito():
    return redirect(url_for('home'))
    
