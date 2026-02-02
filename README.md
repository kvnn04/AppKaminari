⚡ AppKaminari - Frontend E-commerce

Bienvenido al frontend de Kaminari, una plataforma de e-commerce de indumentaria diseñada para ser rápida, segura y totalmente responsiva. Este proyecto nació del desafío de conectar una lógica de negocio compleja con una interfaz de usuario intuitiva.

🚀 Características Principales
Interfaz Dinámica: Carga de productos y vistas de detalle generadas dinámicamente desde la API.

Filtros Inteligentes: Sistema avanzado de filtrado por talle y color mediante persistencia en URL, optimizando la experiencia de usuario y el manejo de estados.

Checkout Integrado: Pasarela de pagos funcional mediante Mercado Pago, permitiendo compras individuales y de carrito completo.

Seguridad: Protección contra ataques CSRF, manejo de sesiones seguras y validaciones de integridad de precios del lado del servidor.

Diseño Mobile-First: Registro, login y catálogo 100% responsivos.

🛠️ Stack Tecnológico
Frontend: HTML5, CSS3, JavaScript (ES6+).

Backend de soporte: Flask (Python).

Pagos: Mercado Pago SDK.

Arquitectura: Implementación de POO en el frontend para organizar la lógica de componentes.

🧠 Desafíos Técnicos y Aprendizajes
Este proyecto fue una verdadera escuela. Aquí detallo los puntos más críticos que resolví:

1. El Dilema de los Filtros (Dropdowns vs Forms)
Inicialmente, los filtros de talle y color estaban dentro de formularios estándar. Esto generaba una fricción innecesaria (clics extra).

Solución: Migré a un sistema de dropdowns con links dinámicos que inyectan parámetros en la URL. Esto permite capturar el estado del producto de forma inmediata para enviarlo al carrito sin recargas innecesarias.

2. Integración de Mercado Pago "a pulmón"
Ante la falta de tutoriales actualizados para la integración con Python/Flask, realicé el despliegue basándome puramente en la documentación oficial.

Logro: Implementé el flujo completo de pago, manejo de credenciales de prueba y aseguré la integridad del precio (evitando que se manipule por URL).

3. Optimización de Logs y Debugging
Tras lidiar con archivos de log de más de 5000 líneas por el reloader de Flask, aprendí a configurar registros específicos para excepciones, permitiendo una trazabilidad real del desarrollo.

📈 Roadmap (Próximas Mejoras)
[ ] Feedback de Usuarios: Implementar sistema de comentarios y reseñas por producto.

[ ] Logística: Agregar formulario de gestión de direcciones de envío.

[ ] Notificaciones: Integrar envío de emails automáticos post-compra con la información del pedido.

📂 Estructura y Metodología
El proyecto se gestionó bajo una metodología de GitFlow simplificada:

Rama main: Código estable y funcional.

Rama develop: Desarrollo de nuevas funcionalidades y pruebas constantes.

Nota del autor: Este proyecto fue un reto personal que me llevó a entender que el Frontend es mucho más que "diseño"; es arquitectura, seguridad y persistencia de datos.
