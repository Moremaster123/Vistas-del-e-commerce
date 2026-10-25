from django.db import migrations

PRODUCTOS = [
    ("Camiseta", "Camiseta de algodón, varias tallas.", "199.00"),
    ("Taza", "Taza de cerámica de 350 ml.", "120.00"),
    ("Gorra", "Gorra ajustable color negro.", "250.00"),
    ("Mochila", "Mochila resistente al agua.", "799.00"),
]


def crear_productos(apps, schema_editor):
    Producto = apps.get_model("ventas", "Producto")
    for nombre, descripcion, precio in PRODUCTOS:
        Producto.objects.create(
            nombre=nombre, descripcion=descripcion, precio=precio
        )


def borrar_productos(apps, schema_editor):
    Producto = apps.get_model("ventas", "Producto")
    Producto.objects.filter(nombre__in=[p[0] for p in PRODUCTOS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("ventas", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(crear_productos, borrar_productos),
    ]
