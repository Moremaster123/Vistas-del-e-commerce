from django.test import TestCase
from django.urls import reverse

from ventas.models import Pedido, Producto


class VentasTests(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre="Libro", precio="100.00"
        )

    def test_lista_de_productos(self):
        response = self.client.get(reverse("ventas:ventas"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Libro")

    def test_agregar_y_quitar_del_carrito(self):
        url = reverse("ventas:agregar", args=[self.producto.id])
        self.client.post(url)
        self.client.post(url)
        response = self.client.get(reverse("ventas:cantidad_carrito"))
        self.assertEqual(response.content, b"2")

        self.client.post(reverse("ventas:quitar", args=[self.producto.id]))
        response = self.client.get(reverse("ventas:cantidad_carrito"))
        self.assertEqual(response.content, b"0")

    def test_procesar_pedido(self):
        self.client.post(reverse("ventas:agregar", args=[self.producto.id]))
        datos = {
            "nombre": "Ana",
            "email": "ana@correo.com",
            "direccion": "Calle 1",
        }
        response = self.client.post(
            reverse("ventas:procesar_pedido"), datos, follow=True
        )

        pedido = Pedido.objects.get()
        self.assertEqual(pedido.total, 100)
        self.assertEqual(pedido.items.count(), 1)
        self.assertContains(response, f"Pedido #{pedido.id} realizado")

    def test_pedido_con_carrito_vacio(self):
        datos = {
            "nombre": "Ana",
            "email": "ana@correo.com",
            "direccion": "Calle 1",
        }
        response = self.client.post(
            reverse("ventas:procesar_pedido"), datos, follow=True
        )
        self.assertEqual(Pedido.objects.count(), 0)
        self.assertContains(response, "Tu carrito está vacío.")

    def test_pedido_con_datos_incorrectos(self):
        self.client.post(reverse("ventas:agregar", args=[self.producto.id]))
        datos = {"nombre": "", "email": "no-es-correo", "direccion": ""}
        response = self.client.post(reverse("ventas:procesar_pedido"), datos)
        self.assertEqual(Pedido.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
