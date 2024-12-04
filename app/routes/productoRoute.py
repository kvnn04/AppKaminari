from typing import List, Literal
from flask import Blueprint, redirect, render_template, flash, url_for
from app.src.forms.selectProducto import ProductFormColor, ProductFormTalle, FilterTalleByColor
from app.logs.capturaDeError import logException
from app.src.token.peticionesProtegidas import getRequest


def filtrarPorTalle(talle, dicti: List[dict]):
    dataByTalle = []
    if not talle:
        return None
    
    dataByTalle = {'talleActual': talle, 'coloresTalleActual': set(), 'opcionesTalle': set()}
    
    for i in dicti:
        if i['talle'] == talle:
            dataByTalle['coloresTalleActual'].add((i['color'],i['color']))
        dataByTalle['opcionesTalle'].add((i['talle'], i['talle']))
    return dataByTalle


producto: Blueprint = Blueprint(name='producto', import_name=__name__)

@producto.route('/<int:id>', methods=['GET', 'POST'])
@producto.route('/<int:id>/<string:talleParams>', methods=['GET', 'POST'])
def productoPage(id: int, talleParams: Literal['xs','s','m','l','xl','xxl','xxxl']|None = None):
    respuesta = getRequest(endpoint="/producto/getProducto", params={'id': id})    
    if respuesta['response'] is None:
        # error = 'no existe este producto'
        logException(exception=Exception(respuesta['message']))
        # flash(message=error)
        return redirect(url_for('home'))
    
    if not respuesta['response']['variantes']:
        return render_template('producto.html', producto = respuesta['response'], errorVariantes='No hay ninguna variante' )
    
 

    if respuesta['response']['id'] == id:

        # lo que tenemos que lograr es hacer un formulario que acepte talle y color, cada vez que yo aprete un option del select
        # se tiene que mandar un redirect, le tengo que pasar ese selec, y en base a ese select voy a hacer que haga el filtro por color
        # una validacion de que si talle existe y color tambien haga un redirect a la compra del producto
        data = respuesta['response']
        variantesData = data['variantes']
        if not talleParams:
            return redirect(url_for('producto.productoPage', id=id, talleParams=variantesData[0]['talle']))

        # choicesTalle = set()
        # choicesColor = set()
        
        dataFilter = filtrarPorTalle(talle=talleParams, dicti=variantesData)
        print(dataFilter)

        # print(dataFilter)

        formUltimo = FilterTalleByColor(talleChoices=list(dataFilter['opcionesTalle']), colorChoices=list(dataFilter['coloresTalleActual']))
        
        if formUltimo.validate_on_submit():
            print(formUltimo.data)
            if not formUltimo.color.data:
                print('SIUUUUUUU')
            return redirect(url_for('producto.productoPage', id=id, talleParams=formUltimo.talle.data))
        
        return render_template('producto.html', producto=respuesta['response'], form=formUltimo, talleActual=talleParams)
    return render_template('pruebas.html', error='Error al encontrar producto')

@producto.route('/<int:id>/<string:talle>')
def productoByTalle(id: int, talle: str, color:str):

    respuesta = getRequest(endpoint="/producto/getProducto", params={'id': id})
    if respuesta['response'] is None:
        # error = 'no existe este producto'
        logException(exception=Exception(respuesta['message']))
        # flash(message=error)
        return redirect(url_for('home'))
    
    # choiceStock = [(str(i), str(i)) for stock in respuesta['response']['variantes'] for i in range(1, stock['stock'] + 1)]

    # print(choiceStock)
    # choicesProduct = {
    #     'talle': [(variantesProducto['talle'], variantesProducto['talle']) for variantesProducto in respuesta['response']['variantes']],
    #     'color':[(varianteProducto['color'], varianteProducto['color']) for varianteProducto in respuesta['response']['variantes']]
    #     }
    # choicesProduct = {
    #     'talle': [talle if talle in respuesta['response']['variantes']['talle'] else []],
    #     'color':[(varianteProducto['color'], varianteProducto['color']) for varianteProducto in respuesta['response']['variantes']]
    #     }
    tlle = []
    for i in respuesta['response']['variantes']:
        if talle in i['talle'] and not tlle:
            tlle.append((talle,talle))
    colorr = []
    for i in respuesta['response']['variantes']:
        if color in i['color'] and not colorr:
            colorr.append((color,color))

    print(tlle,colorr)
    dic = {'talle': tlle, 'color': colorr}
    # formProducto: ProductForm = ProductForm(colorChoices=choicesProduct)
    return render_template('pruebas.html', pruebas=dic)