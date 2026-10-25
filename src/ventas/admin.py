from django.contrib import admin

from ventas.models import ItemPedido, Pedido, Producto

admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
