from typing import List, Literal
from flask import Blueprint, redirect, render_template, flash, url_for
from app.src.forms.selectProducto import ProductFormColor, ProductFormTalle, FilterTalleByColor
from app.logs.capturaDeError import logException
from app.src.token.peticionesProtegidas import getRequest

def getCantidadByProducto(cantidad: int)->List[str]:    
    limit = 10
    contador = 0
    lista = []
    while contador < limit and contador < cantidad:
        contador+=1
        lista.append(str(contador))
    return lista

def filtrarPorTalle(talle, listaVariantes: List[dict]):
    dataByTalle = []
    if not talle:
        return None
    dataByTalle = {'coloresTalleActual': set(), 'talleDisponible': set()}
    for i in listaVariantes:
        if i['talle'] == talle:
            dataByTalle['coloresTalleActual'].add(i['color'])
        dataByTalle['talleDisponible'].add(i['talle'])
    
    dataByTalle['coloresTalleActual'] = list(dataByTalle['coloresTalleActual'])
    dataByTalle['talleDisponible'] = list(dataByTalle['talleDisponible'])

    return dataByTalle


def getStock(listaVariantesProducto: List[dict], talle: str, color: str):
    for i in listaVariantesProducto:
        if i['talle'] == talle and i['color'] == color:
            return i['stock']
def totalTalleAndColorForVerify(lista: List[dict]):
    data = {'totalColores': set(), 'totalTalle': set()}
    for i in lista:
        data['totalColores'].add(i['color'])
        data['totalTalle'].add(i['talle'])
    
    data['totalColores'] = list(data['totalColores'])
    data['totalTalle'] = list(data['totalTalle'])
    return data

producto: Blueprint = Blueprint(name='producto', import_name=__name__)

@producto.route('/<int:id>', methods=['GET', 'POST'])
@producto.route('/<int:id>/<string:talleParams>', methods=['GET', 'POST'])
@producto.route('/<int:id>/<string:talleParams>/<string:colorParams>/<int:cantidadParams>', methods=['GET', 'POST'])
def productoPage(id: int, talleParams: Literal['xs','s','m','l','xl','xxl','xxxl']|None = None, colorParams: str|None = None, cantidadParams: int|None = None):

    respuesta = getRequest(endpoint=f"/producto/{id}", params={'id': id})

        # if talleParams is None or colorParams is None or cantidadParams is None:
    if not respuesta['response']:
        
        logException(exception=Exception(respuesta['message']))
        return redirect(url_for('home'))
    
    if not respuesta['response']['variantes']:
        return render_template('producto.html', producto = respuesta['response'], errorVariantes='No hay ninguna variante')
    
    if respuesta['response']['id'] == id:

        if talleParams is not None and colorParams is None and cantidadParams is None:
            primerColorYTalleDisponiblesByProductos=filtrarPorTalle(listaVariantes=respuesta['response']['variantes'], talle=talleParams)
            return redirect(url_for('producto.productoPage', id=respuesta['response']['id'], talleParams=talleParams, colorParams=primerColorYTalleDisponiblesByProductos['coloresTalleActual'][0], cantidadParams=1))
        
        if talleParams is None or colorParams is None or cantidadParams is None:
            primerVarianteDeProducto = respuesta['response']['variantes'][0]
            return redirect(url_for('producto.productoPage', id=respuesta['response']['id'], talleParams=primerVarianteDeProducto['talle'], colorParams=primerVarianteDeProducto['color'], cantidadParams=1))
        
        totalessForVerify = totalTalleAndColorForVerify(lista=respuesta['response']['variantes'])

        if talleParams not in totalessForVerify['totalTalle']:
            return redirect(url_for('home'))
        if colorParams not in totalessForVerify['totalColores']:
            return redirect(url_for('home'))

        colorYTalleDisponiblesByProductos=filtrarPorTalle(listaVariantes=respuesta['response']['variantes'], talle=talleParams)

        stock = getStock(listaVariantesProducto=respuesta['response']['variantes'], talle=talleParams, color=colorParams)

        if cantidadParams > stock:
            return redirect(url_for('home'))
        
        cantidadDisponible = getCantidadByProducto(cantidad=stock)
        dataProducto = { 'id': id, 'nombreProducto': respuesta['response']['nombre'], 'precio': respuesta['response']['precio'] ,'talleParams': talleParams, 'colorParams' : colorParams, 'cantidadParams' : cantidadParams, 'stockVariante': stock ,'cantidadDisponible' : cantidadDisponible, 'colorYTalleDisponiblesByProductos': colorYTalleDisponiblesByProductos}
        return render_template('producto.html', producto=respuesta['response'], dataProducto=dataProducto)
    

    return render_template('producto.html', producto=respuesta['response'])
