# Primero la interfaz que va a tener que cumplir mi clase

from abc import ABC, abstractmethod

class InterfazUsuario(ABC):

    @property
    @abstractmethod
    def nombre():
        pass
    @property
    @abstractmethod
    def apellido():
        pass
    @property
    @abstractmethod
    def email():
        pass
    @property
    @abstractmethod
    def username():
        pass

class Usuario(InterfazUsuario):
    def __init__(self, nombre: str, apellido: str, email: str, username: str) -> None:
        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__username = username
    
    @property
    def nombre(self) -> str:
        if type(self.__nombre) != str|bool:
            return False
        return self.__nombre
    
    @property
    def apellido(self) -> str|bool:
        if type(self.__apellido) != str|bool:
            return False
        return self.__apellido
    
    @property
    def email(self) -> str:
        if type(self.__email) != str|bool:
            return False
        return self.__email
    
    @property
    def nombre(self) -> str:
        if type(self.__username) != str|bool:
            return False
        return self.__username