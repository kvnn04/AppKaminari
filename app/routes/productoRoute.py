from typing import List, Literal
from flask import Blueprint, redirect, render_template, flash, url_for
from app.src.forms.selectProducto import ProductFormColor, ProductFormTalle, FilterTalleByColor
from app.logs.capturaDeError import logException
from app.src.token.peticionesProtegidas import getRequest

def filtrarPorTalle(talle, listaVariantes: List[dict]):
    dataByTalle = []
    if not talle:
        return None
    
    dataByTalle = {'talleActual': talle, 'coloresTalleActual': set(), 'opcionesTalle': set(), 'stock': set()}
    
    for i in listaVariantes:
        if i['talle'] == talle:
            dataByTalle['coloresTalleActual'].add((i['color'],i['color']))
            dataByTalle['stock'].add(i['stock'])
        dataByTalle['opcionesTalle'].add((i['talle']))
    return dataByTalle

def getStock(listaVariantesProducto: List[dict], talle: str, color: str):
    for i in listaVariantesProducto:
        if i['talle'] == talle and i['color'] == color:
            return i['stock']


producto: Blueprint = Blueprint(name='producto', import_name=__name__)

@producto.route('/<int:id>', methods=['GET', 'POST'])
@producto.route('/<int:id>/<string:talleParams>', methods=['GET', 'POST'])
@producto.route('/<int:id>/<string:talleParams>/<string:colorParams>', methods=['GET', 'POST'])
def productoPage(id: int, talleParams: Literal['xs','s','m','l','xl','xxl','xxxl']|None = None, colorParams: str|None = None):
    respuesta = getRequest(endpoint="/producto/getProducto", params={'id': id})    
    if not respuesta['response']:
        
        logException(exception=Exception(respuesta['message']))
        return redirect(url_for('home'))
    
    if not respuesta['response']['variantes']:
        return render_template('producto.html', producto = respuesta['response'], errorVariantes='No hay ninguna variante' )
    
    if respuesta['response']['id'] == id:

        if talleParams is None:
            idProducto=respuesta['response']['id']
            primerVarianteProducto = respuesta['response']['variantes'][0]
            return redirect(url_for('producto.productoPage', id=idProducto, talleParams=primerVarianteProducto['talle'], colorParams=primerVarianteProducto['color']))

        if talleParams is not None and colorParams is None:
            idProducto=respuesta['response']['id']
            dataRespuestaOfProducto = respuesta['response']
            variantesDataFromProducto = dataRespuestaOfProducto['variantes'] # Variantes seria ej: {'talle': 's', 'color': 'verde', 'stock': 5} , relacionado a un producto. Puede tener muchas "Variantes
            dataFilterByTalle = filtrarPorTalle(talle=talleParams, listaVariantes=variantesDataFromProducto)
            print(dataFilterByTalle['coloresTalleActual'], 'lpasfasdfbokaaaaaaaaaaaaaaa')
            primerColor = list(dataFilterByTalle['coloresTalleActual'])[0][0]
            return redirect(url_for('producto.productoPage', id=idProducto, talleParams=dataFilterByTalle['talleActual'], colorParams=primerColor))
        
        
        n = respuesta['response']['variantes']
        
        # # print(n,'asdfasdfasdfasdfasdf')
        # stockProducto = 
        # print(stockProducto)
        


        dataFilterByTalle = filtrarPorTalle(talle=talleParams, listaVariantes=n)
        dataFilterByTalle['opcionesTalle'] = list(dataFilterByTalle['opcionesTalle']) 
        dataFilterByTalle['coloresTalleActual'] = list(dataFilterByTalle['coloresTalleActual'])
        dataFilterByTalle['stockFromTalleActual'] = getStock(n, talle=talleParams, color=colorParams)
        # print(dataFilterByTalle)
        return render_template('producto.html', producto=respuesta['response'], talleActual=dataFilterByTalle, colorParams=colorParams )
        