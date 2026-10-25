from django.urls import path

from ventas import views

app_name = "ventas"

urlpatterns = [
    path("", views.ventas, name="ventas"),
    path(
        "agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar"
    ),
    path("quitar/<int:producto_id>/", views.quitar_del_carrito, name="quitar"),
    path("vaciar/", views.vaciar_carrito, name="vaciar"),
    path("pedido/", views.procesar_pedido, name="procesar_pedido"),
    path("carrito/cantidad/", views.cantidad_carrito, name="cantidad_carrito"),
]
