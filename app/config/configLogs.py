import logging
from pathlib import Path


log_path = Path("app/logs/appErrors.log")

# Crear loggers separados para consola y archivo
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)  # Solo se mostrarán errores en consola

file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.ERROR)  # Solo se guardarán errores en el archivo

# Configuración de logging
logging.basicConfig(
    level=logging.CRITICAL,  # Registra solo los errores a partir de este nivel
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[console_handler, file_handler]  # Añadir ambos handlers
)

# '''
# El mensaje "Restarting with stat" es generado por el servidor de desarrollo de Flask (utilizando werkzeug), 
# que indica que el servidor se está reiniciando debido a cambios en los archivos. Aunque ajustaste el nivel 
# de logging a ERROR, este tipo de mensajes se siguen mostrando porque son generados por el servidor de desarrollo
#  y no están completamente controlados por el nivel de logging que configuraste.
# '''
# log = logging.getLogger('werkzeug')  # El logger de Werkzeug maneja los logs de Flask
# log.setLevel(logging.CRITICAL)  # Esto debería evitar que registre nada, incluyendo INFO
# log.handlers = []