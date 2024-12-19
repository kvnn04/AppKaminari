# SDK de Mercado Pago
from flask import Blueprint, jsonify, redirect, request, url_for, session
from app.config.sdkMp import sdk
from app.logs.capturaDeError import logException
from app.src.token.peticionesProtegidas import getRequest

pagoProductoRoute = Blueprint('pagoProducto', import_name=__name__)

@pagoProductoRoute.route('/<int:id>/<int:cantidad>', methods=['POST', 'GET'])
def pagos(id: int, cantidad: int):

    productoPrecio = getRequest('/producto/getPrecio', params={'id': id})

    if not productoPrecio['response']:
        return redirect(url_for('home'))

    user = session.get('informationUsuario', [])

    if not user:
        print(user)
        return redirect(url_for('home'))
    try:
        # print(url_for('pago.notifications', _external=True))
        preference_data = {
            "items": [
                {
                    "title": 'holaa',
                    "quantity": int(cantidad),
                    "currency_id": "ARS",  # Moneda
                    "unit_price": float(productoPrecio['response'])    # Precio unitario
                }
            ],
            "back_urls": {
                "success": url_for('pagoProducto.paymentProductoSuccess', _external=True),
                "failure": "http://localhost:5000/failure",
                "pending": "http://localhost:5000/pending"
            },

            # "external_reference": "ORDEN12345",  # Puedes cambiarlo por un ID único generado por tu sistema
            "payer": {
                "name": user['nombre'],
                "email": user['email']
            },
            # "notification_url": "http://localhost:5000/pago/notificationss"
        }
        preference_response = sdk.preference().create(preference_data)
        preference_url = preference_response["response"]["init_point"]  # URL para redirigir al usuario
    except Exception as e:
        logException(Exception)
        print(f"Error: {e}")
    return redirect(preference_url)




@pagoProductoRoute.route('/paymentProductoSuccess', methods=['GET'])
def paymentProductoSuccess():
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
    
