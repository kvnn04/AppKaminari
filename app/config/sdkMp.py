import mercadopago
from dotenv import load_dotenv
from os import getenv

load_dotenv(dotenv_path='dataSensible.env')

sdk = mercadopago.SDK(getenv('SDKMP'))

# aca va eso pero en variable de entorno