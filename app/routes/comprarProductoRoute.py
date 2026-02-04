# SDK de Mercado Pago
from flask import Blueprint, flash, jsonify, redirect, request, url_for, session
from app.config.sdkMp import sdk
from app.logs.capturaDeError import logException
from app.src.token.peticionesProtegidas import getRequest

pagoProductoRoute = Blueprint('pagoProducto', import_name=__name__)

@pagoProductoRoute.route('/<int:id>/<int:cantidad>', methods=['POST', 'GET'])
def pagos(id: int, cantidad: int):

    '''
    Tiene que existir:
        -Usuario
        -DireccionUsuario
    Sino existe esto lo que va a ser es redireccionar a home

    PENDIENTE: tengo que avisarle al usuario, mostrar un tipo de mensaje
    '''
    productoPrecio = getRequest(f'/producto/{id}/precio', params={'id': id})
    if not productoPrecio['response']:
        flash("Hubo un error interno", "info") # UX: Avisar por qué rediriges
        return redirect(url_for('home'))

    user = session.get('informationUsuario', [])

    if not user:

        session['urlPrevio'] = request.url
        flash("Debes iniciar sesión para comprar", "warning")
        return redirect(url_for('signIn.iniciarSesion'))
    
    direccionUsuario: dict[str, str] = session.get('direccionUsuario', [])

    if not direccionUsuario:
        session['urlPrevio'] = request.url
        return redirect(url_for('direccion.direccionUsuario'))

    try:
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
                "failure": url_for('pagoProducto.paymentFailedProducto', _external=True),
                "pending": url_for('pagoProducto.paymentPendingProducto', _external=True)
            },
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
        # print(f"Error: {e}")
    return redirect(preference_url) # type: ignore



@pagoProductoRoute.route('/paymentProductoSuccess', methods=['GET'])
def paymentProductoSuccess():
    # Aquí puedes capturar y procesar los datos que vienen por la URL
    payment_id = request.args.get('payment_id')  # Ejemplo: Obtener un parámetro llamado 'payment_id'
    status = request.args.get('status')         # Otro ejemplo: Obtener el estado del pago
    
    # # Opcional: Guardar los datos en sesión o en una base de datos
    # if payment_id and status:
    #     session['payment_info'] = {
    #         'payment_id': payment_id,
    #         'status': status
    #     }

    session.permanent = True  # Refresca el tiempo de expiración cuando se accede

    
    if 'direccionUsuario' in session:
        session.pop('direccionUsuario')
        session.modified = True

    # Redirige a 'home' sin los datos adicionales en la URL
    return redirect(url_for('home'))

@pagoProductoRoute.route('/paymentFailed', methods=['GET'])
def paymentFailedProducto():
    direccionUsuario = session.get('direccionUsuario', [])
    if direccionUsuario:
        session['direccionUsuario'] = []  # Actualiza en la sesión
        session.modified = True
    return redirect(url_for('home'))

@pagoProductoRoute.route('/paymentPending', methods=['GET'])
def paymentPendingProducto():
    return redirect(url_for('home'))
    
