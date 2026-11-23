# Vistas del e-commerce

App de ventas hecha con vistas de Django: catálogo de productos, carrito guardado en la sesión y formulario para hacer el pedido. Forma parte de la serie de tareas del proyecto e-commerce de la profesión Full Stack Python de EBAC. Cada repositorio guarda el proyecto como quedó al terminar ese tema; la versión final es [e-commerce-completo](https://github.com/Moremaster123/e-commerce-completo).

Para este tema usé como base la plantilla [docker-django-example](https://github.com/nickjj/docker-django-example) de Nick Janetakis (licencia MIT), que ya trae Docker configurado. Mi trabajo está en la app `src/ventas`.

## Tecnologías

- Python y Django 6.0
- Docker Compose con PostgreSQL, Redis y un worker de Celery
- Tailwind CSS y esbuild para los estilos y el JavaScript
- GitHub Actions para correr las pruebas

## Qué hace la app `ventas`

- Muestra los productos con su precio.
- Agrega y quita productos del carrito, o lo vacía. El carrito vive en la sesión del usuario.
- Calcula el total y guarda el pedido con nombre, correo y dirección (`Pedido` e `ItemPedido`).
- Devuelve la cantidad de productos del carrito para mostrarla en el menú.

| Ruta | Qué hace |
|---|---|
| `/ventas/` | Catálogo, carrito y formulario de pedido |
| `/ventas/quitar/<id>/` | Quita un producto del carrito |
| `/ventas/vaciar/` | Vacía el carrito |
| `/ventas/pedido/` | Guarda el pedido |
| `/ventas/carrito/cantidad/` | Cantidad de productos en el carrito |

## Cómo ejecutarlo

Necesitas Docker Desktop.

```bash
cp .env.example .env
docker compose up --build
```

En otra terminal crea las tablas y un administrador:

```bash
./run manage migrate
./run manage createsuperuser
```

Abre `http://localhost:8000/ventas/`. Los productos se dan de alta desde `http://localhost:8000/admin/`.

## Pruebas

```bash
./run manage test
```

## Autor

Juan Carlos González Herrera · [LinkedIn](https://www.linkedin.com/in/juan-carlos-desarrollador-web) · [Portafolio](https://moremaster123.github.io)
