from decimal import Decimal

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from ventas.forms import PedidoForm
from ventas.models import ItemPedido, Producto


def obtener_carrito(request):
    return request.session.get("carrito", {})


def guardar_carrito(request, carrito):
    request.session["carrito"] = carrito


def detalle_carrito(carrito):
    items = []
    total = Decimal(0)
    for producto in Producto.objects.filter(id__in=carrito.keys()):
        cantidad = carrito[str(producto.id)]
        subtotal = producto.precio * cantidad
        total += subtotal
        items.append(
            {"producto": producto, "cantidad": cantidad, "subtotal": subtotal}
        )
    return items, total


def ventas(request, form=None):
    items, total = detalle_carrito(obtener_carrito(request))
    context = {
        "productos": Producto.objects.all(),
        "items": items,
        "total": total,
        "form": form or PedidoForm(),
    }
    return render(request, "ventas/ventas.html", context)


@require_POST
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = obtener_carrito(request)
    clave = str(producto.id)
    carrito[clave] = carrito.get(clave, 0) + 1
    guardar_carrito(request, carrito)
    messages.success(request, f"{producto.nombre} se agregó al carrito.")
    return redirect("ventas:ventas")


@require_POST
def quitar_del_carrito(request, producto_id):
    carrito = obtener_carrito(request)
    carrito.pop(str(producto_id), None)
    guardar_carrito(request, carrito)
    return redirect("ventas:ventas")


@require_POST
def vaciar_carrito(request):
    guardar_carrito(request, {})
    return redirect("ventas:ventas")


@require_POST
def procesar_pedido(request):
    items, total = detalle_carrito(obtener_carrito(request))
    if not items:
        messages.error(request, "Tu carrito está vacío.")
        return redirect("ventas:ventas")

    form = PedidoForm(request.POST)
    if not form.is_valid():
        return ventas(request, form)

    pedido = form.save(commit=False)
    pedido.total = total
    pedido.save()
    ItemPedido.objects.bulk_create(
        ItemPedido(
            pedido=pedido,
            producto=item["producto"],
            cantidad=item["cantidad"],
            precio=item["producto"].precio,
        )
        for item in items
    )
    guardar_carrito(request, {})
    messages.success(
        request, f"Pedido #{pedido.id} realizado. Total: ${total}"
    )
    return redirect("ventas:ventas")


def cantidad_carrito(request):
    return HttpResponse(sum(obtener_carrito(request).values()))
