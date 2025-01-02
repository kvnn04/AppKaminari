import os
from flask import Flask, flash, redirect, render_template, session, url_for
# from requests import Session, session
from flask_session import Session
from redis import Redis
from app.logs.capturaDeError import logException
from app.routes.logOutRoute import logOut
from app.routes.usuarioRoute import usuario
from app.routes.productoRoute import producto
from app.routes.registerRoute import signUp
from app.routes.iniciarSesionRoute import signIn
from app.routes.carritoRoute import carrito
from app.routes.comprarProductoRoute import pagoProductoRoute
from app.routes.comprarCarritoRoute import pagoCarritoRoute
from app.routes.direccionRoute import direccionRoute
from flask_wtf.csrf import CSRFProtect
from app.src.token.peticionesProtegidas import getRequest
from dotenv import load_dotenv
from os import getenv
from datetime import time, timedelta


load_dotenv(dotenv_path='dataSensible.env')

app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
csrf: CSRFProtect = CSRFProtect(app=app)

app.register_blueprint(usuario, url_prefix='/usuario')
app.register_blueprint(producto, url_prefix='/producto')
app.register_blueprint(signUp, url_prefix='/register')
app.register_blueprint(signIn, url_prefix='/signIn')
app.register_blueprint(carrito, url_prefix='/carrito')
app.register_blueprint(logOut, url_prefix='/logOut')
app.register_blueprint(pagoProductoRoute, url_prefix='/pagoProducto')
app.register_blueprint(pagoCarritoRoute, url_prefix='/pagoCarrito')
app.register_blueprint(direccionRoute, url_prefix='/direccion')

# # Configuración de Flask-Session
# app.config["SESSION_TYPE"] = "filesystem"  # Usar sistema de archivos
# app.config["SESSION_FILE_DIR"] = "flask_session"  # Directorio para sesiones
# app.config["SESSION_PERMANENT"] = True
# app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=60)
# app.config["SESSION_USE_SIGNER"] = True  # Firmar cookies de sesión
# app.config["SESSION_FILE_THRESHOLD"] = 5  # Máximo número de sesiones antes de limpiar
# app.config["SESSION_COOKIE_SECURE"] = False  # HTTPS solo (ajusta según producción)
# app.config["SESSION_COOKIE_HTTPONLY"] = True

# # Configuración de sesiones
# app.config["SESSION_PERMANENT"] = True
# app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
# app.config["SESSION_USE_SIGNER"] = True
# app.config["SESSION_COOKIE_SECURE"] = True
# app.config["SESSION_COOKIE_HTTPONLY"] = True

key = getenv('SECRET_KEY')
# Configuración de Redis para almacenar las sesiones
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=30)  # Sesión expira después de 30 minutos
app.config["SESSION_USE_SIGNER"] = True  # Firmar las claves de sesión para mayor seguridad
app.config["SESSION_KEY_PREFIX"] = "session:"  # Prefijo para las claves de sesión
app.config["SESSION_COOKIE_SECURE"] = True  # Hacer las cookies solo accesibles a través de HTTPS
app.config["SESSION_COOKIE_HTTPONLY"] = True  # No accesible por JavaScript
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"  # Prevenir CSRF (Cross Site Request Forgery)

app.config["SECRET_KEY"] = key  # Clave secreta para firmar la sesión
if key:

# try:
#     redis_client = Redis(host="localhost", port=6378, password="MiClaveSuperSecreta")
#     redis_client.ping()
#     print("Conexión exitosa a Redis")
# except Exception as e:
#     print(f"Error conectando a Redis: {e}")

# Proveer una instancia de Redis
    app.config["SESSION_REDIS"] = Redis(host="localhost", port=6379)


    Session(app=app)

@app.route('/')
def home():
    # acordarme de session
    respuesta = getRequest(endpoint="/producto/getAllProducto")

    print(session)
    
    if respuesta['response'] is None:
        error = 'Error'
        cont=0
        if cont < 1:
            logException(exception=Exception(respuesta['message']))
            flash(message=error)
            cont+=1
        return redirect(url_for('home'))
    # Paso imagenes de mas del lado del front si hay mas de una imagen va ir igual, pero lo que hago es agarrar el primero, pero me molesta pasar informacion de mas

    return render_template('index.html', allproduct = respuesta['response'])
