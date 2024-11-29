

from typing import Literal
import requests
from app.config.urlMiApi import BASE_URL
from app.logs.capturaDeError import logException


def protectedRequest(endpoint, token: str|None= None, method = Literal['get', 'put', 'delete'], data=None) -> dict:
    url = f"{BASE_URL}{endpoint}"
    token = token
    # print(token)
    if not token:
        return {'response': None, 'message': 'No existe el token'}
    headers = {"Authorization": f"Bearer {token}"}
    if method.lower() == 'get':
        response = requests.get(url, headers=headers)
    if method.lower()=='put':
        if not data:
            return {'response': None, 'message': 'Agrega lo que queres modificar en data'}
        response = requests.put(url, headers=headers, json=data)
    if method.lower() == 'delete':
        response = requests.delete(url, headers=headers)

    

    # if response.status_code == 401:  # Token expirado
    #     print("Token expirado. Reautenticando...")
    #     headers = {"Authorization": f"Bearer {authenticate('testuser', 'testpassword')}"}
    #     response = requests.get(url, headers=headers)
    #     #redirigir aca
    if response.status_code == 200:
        return {'response': response.json()}
    
    return {'response': None, 'message': 'Error en el status de la respuesta'}

def postRequest(endpoint: str, data: dict, token: str | None = None):
    url = f"{BASE_URL}{endpoint}"
    try:
        if not data:
            return {'response': None, 'message': 'Agrega lo que queres mandar en data'}
        
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
                # error_message = response.json().get("detail", "Error desconocido")
                error_message = response.json().get('detail', 'Error en la peticion')
                return {'response': None, 'message': f'{error_message}'}

        return {'response': response.json(), 'message': 'Éxito'}
    except Exception as e:
        logException(e)
        return {'response': None, 'message': f'Hubo una excepción: {str(e)}'}
    
def getRequest(endpoint: str, token: str | None = None, params: dict|None = None):
    url = f"{BASE_URL}{endpoint}"
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        params = params if params else {}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
                error_message = response.text
                return {'response': None, 'message': f'Error en la petición: {error_message}'}

        return {'response': response.json(), 'message': 'Éxito'}
    except Exception as e:
        logException(e)
        return {'response': None, 'message': f'Hubo una excepción: {str(e)}'}
