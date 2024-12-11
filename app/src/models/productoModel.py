# Primero la interfaz que va a tener que cumplir mi clase

from abc import ABC, abstractmethod
from typing import List

class InterfazProducto(ABC):

    @abstractmethod
    def __init__():
        pass

    @property
    @abstractmethod
    def id():
        pass
    @property
    @abstractmethod
    def nombre():
        pass
    
    @property
    @abstractmethod
    def precio():
        pass
    @property
    @abstractmethod
    def talle():
        pass

class Producto(InterfazProducto):

    def __init__(self, id: int, nombre: str, precio: float, talle: str):
        self.__id: int = id
        self.__nombre: str = nombre
        self.__precio: float = precio
        self.__talle: str = talle
    
    
    @property
    def id(self):
        return self.__id
    @property
    def nombre(self):
        return self.__nombre
    @property
    def precio(self):
        return self.__precio
    @property
    def talle(self):
        return self.__talle
