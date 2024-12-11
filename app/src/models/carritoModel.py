# Primero la interfaz que va a tener que cumplir mi clase

from abc import ABC, abstractmethod
from typing import List
from app.src.models.productoModel import Producto

class InterfazCarrito(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @property
    @abstractmethod
    def producto(self):
        pass

    @abstractmethod
    def agregarProducto(self):
        pass

class Carrito(InterfazCarrito):

    def __init__(self):
        super().__init__()
        self.__producto: List[Producto] = []
    
    @property
    def producto(self):
        return self.__producto
    
    def agregarProducto(self, producto: Producto):
        self.__producto.append(producto)
        
    def calcularTotalPrecio(self):
        totalPrecio: float = 0
        for i in self.__producto:
            if not i.precio:
                return 'No existe Precio'
            totalPrecio += float(i.precio)
