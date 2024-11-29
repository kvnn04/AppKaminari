import requests

from app.config.urlMiApi import BASE_URL
from app.logs.capturaDeError import logException

def authenticate(username, password) -> None|str:
    url = f"{BASE_URL}/token"
    data = {"username": username, "password": password}
    response = requests.post(url, data=data)
    if response.status_code != 200:
      logException(Exception(response.text))
      return None
      #  print(f'Error al obtener el token: {response.text}')
    token: str = response.json().get("access_token")
    return token

