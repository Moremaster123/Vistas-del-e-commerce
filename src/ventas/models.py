from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    direccion = models.CharField(max_length=200)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.nombre}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="items"
    )
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto}"
