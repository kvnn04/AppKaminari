from flask import Flask, flash, redirect, render_template, session, url_for
from app.logs.capturaDeError import logException
from app.routes.logOutRoute import logOut
from app.routes.usuarioRoute import usuario
from app.routes.productoRoute import producto
from app.routes.registerRoute import signUp
from app.routes.iniciarSesionRoute import signIn
from app.routes.carritoRoute import carrito
from app.routes.comprarProductoRoute import pagoProductoRoute
from app.routes.comprarCarritoRoute import pagoCarritoRoute
from flask_wtf.csrf import CSRFProtect
from app.src.token.peticionesProtegidas import getRequest

app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = 'MiClaveSuperSecreta'
csrf: CSRFProtect = CSRFProtect(app=app)

app.register_blueprint(usuario, url_prefix='/usuario')
app.register_blueprint(producto, url_prefix='/producto')
app.register_blueprint(signUp, url_prefix='/register')
app.register_blueprint(signIn, url_prefix='/signIn')
app.register_blueprint(carrito, url_prefix='/carrito')
app.register_blueprint(logOut, url_prefix='/logOut')
app.register_blueprint(pagoProductoRoute, url_prefix='/pagoProducto')
app.register_blueprint(pagoCarritoRoute, url_prefix='/pagoCarrito')


@app.route('/')
def home():
    # acordarme de session
    respuesta = getRequest(endpoint="/producto/getAllProducto")
    if respuesta['response'] is None:
        error = 'Error al registrarse'
        logException(exception=Exception(respuesta['message']))
        flash(message=error)
        return redirect(url_for('home'))

    return render_template('index.html', allproduct = respuesta['response'])
