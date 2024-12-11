# AppKaminari
Esta es la parte del front de mi web

dia: 4/12/2024
    Me cuesta una banda la parte del frontend, pero por ahora vamos muy bien, puntos fuertes resueltos:
        -Registro_responsivo
        -IniciarSesion_responsivo  
        -Vista del main_responsivo
        -Agregado de Productos a main dinamico
        -Vista del productos_responsivo
        -link a vista de producto en especifico de manera dinamica
        -Carrusel agregado a vista de productos
        -Filtro por talle en la vista productos
        -Proteccion contra CSRF
        -Creo que es bueno una cantidad reducida de peticiones a mi api

        Puntos malos: 
            -Estructura de proyecto esta mal para mi, creeo
            -Nose mucho el como aplicar los patrones GRASP en la parte del front, eso no significa que no lo haya usado
            -Me olvide de las imagenes de los productos, agregarlos en la base de datos
        
        Pendientes:
            -Agregar una funcion js para que se actualize los colores por talle de manera automatica
            -Agregar imagenes para mis productos
            -Mejorar mi header
            -Agregar para que personas puedan comentar mis productos
            -Agregar MercadoPago


dia 11/12/2024:

    -Encontre con problemas con en la parte de filtrado de talle y color en la pagina de productos y los resolvi,
    tenia pensado que los select esten adentro de un form, y cuando lo aprete me traiga lo filtrado osea agregarle un js que lo que haga sea un escuchador para cuando se aprete el select, pero esto lo que hacia era que si o si tenga que apretar el submit(btn) entonces para cuando quiero guardar un producto en carrito, ¿ como haria para obtener ese color? entonces lo que hice fue hacer no select sino hacer un dropdown con links, y le paso por parametro a la url el talle y el color, asi cuando quiera hacer cualquier cosa con esos datos los traigo ya de la url misma.
    -trato de implementar POO en la parte esta que seria front, ( pq verga pensaba que en el front no se utilizaba POO, me hubiera resultado hacer todo mas sencillo)
    -Queria que los registros en los logs solo sean de excepciones pero la mrd esa me tomaba el reload de la aplicacion como un log, y ahora tengo un archivo de 5000 lineas de logs alpedo, yo queria que eso fuera mi registro de recorrido, que si estoy haciendo el proyecto.
    No lo pienso borrar, ya que ahi tiene las fechas de que yo le dedique mucho tiempo a esta basura.

    pendientes:
        -Agregar imagenes para mis productos
        -Mejorar mi header
        -Agregar para que personas puedan comentar mis productos
        -Agregar MercadoPago

    (Que dificiiiiiiil, creo que quiero morir o aunque sea darle un viaje a mi compu)

    