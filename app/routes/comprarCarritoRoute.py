# SDK de Mercado Pago
from typing import List
from flask import Blueprint, flash, jsonify, redirect, request, url_for, session
from app.config.sdkMp import sdk
from app.logs.capturaDeError import logException
from app.src.token.peticionesProtegidas import getRequest

pagoCarritoRoute = Blueprint('pagoCarrito', import_name=__name__)

@pagoCarritoRoute.route('/', methods=['POST', 'GET'])
def pagoCarrito():
    productosInCarrito = session.get('carrito', [])

    if not productosInCarrito:
        flash("Tu carrito está vacío", "info") # UX: Avisar por qué rediriges
        return redirect(url_for('carrito.carritoPage'))
    
    user = session.get('informationUsuario')
    if not user:
        session['urlPrevio'] = request.url
        flash("Debes iniciar sesión para comprar", "warning")
        return redirect(url_for('signIn.iniciarSesion'))
    
    direccionUsuario = session.get('direccionUsuario')
    if not direccionUsuario:
        session['urlPrevio'] = request.url
        # flash("Por favor, completa tu dirección de envío", "warning")
        return redirect(url_for('direccion.direccionUsuario'))

    idsProductosInCarrito = [item.get('id') for item in productosInCarrito if 'id' in item]
        
    try:
        response_api = getRequest('/producto/precios', params={'ids': idsProductosInCarrito})
        productoPrecio = response_api.get('response', [])
        
        preciosPorId = {str(item['id']): item['precio'] for item in productoPrecio}
        preference_data = {
            "items": [],
            "back_urls": {
                "success": str(url_for('pagoCarrito.paymentSuccessCarrito', _external=True)),
                "failure": str(url_for('pagoCarrito.paymentFailedCarrito', _external=True)),
                "pending": str(url_for('pagoCarrito.paymentPendingCarrito', _external=True))
            },
            "payer": {
                "name": str(user.get('username')),
                "email": str(user.get('email')) 
            },
            # Es una buena práctica agregar una referencia externa para tu control
            "external_reference": "PEDIDO_12345", 
        }

        for i in productosInCarrito:
            # Buscamos el precio en la respuesta de la API usando el ID
            id_actual = str(i.get('id'))
            precio_valido = preciosPorId.get(id_actual)

            # Si el precio no vino en la API, usamos el de la sesión o fallamos por seguridad
            if precio_valido is None:
                precio_valido = i.get('precio', 0)

            data = {
                "title": str(i.get('nombre', 'Producto KHANTANI')),
                "quantity": int(i.get('cantidad', 1)),       # Forzamos a entero
                "currency_id": "ARS",
                "unit_price": float(precio_valido)           # Forzamos a float
            }
            
            # UX/UI Preventiva: No enviamos ítems con precio 0 o cantidad 0
            if data['quantity'] > 0 and data['unit_price'] > 0:
                preference_data['items'].append(data)
        
        # Crear preferencia
        preference_response = sdk.preference().create(preference_data)
        
        if preference_response["status"] == 201 or preference_response["status"] == 200:
            if 'direccionUsuario' in session:
                session.pop('direccionUsuario')
                session.modified = True
            return redirect(preference_response["response"]["init_point"])
        else:
            # Aquí verás el error real en tu consola
            print("Detalle de error de MP:", preference_response["response"])
            raise Exception(f"Mercado Pago falló con status {preference_response['status']}")

    except Exception as e:
        print(f"Error en el proceso de pago: {e}")
        flash("No pudimos conectar con la pasarela de pago. Reintenta en unos minutos.", "danger")

        if 'direccionUsuario' in session:
            session.pop('direccionUsuario')
            session.modified = True
        return redirect(url_for('carrito.carritoPage'))


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
    
