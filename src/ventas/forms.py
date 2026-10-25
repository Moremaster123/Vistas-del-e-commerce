from django import forms

from ventas.models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ("nombre", "email", "direccion")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "w-full border border-gray-300 rounded px-3 py-2"
            )
        self.fields["direccion"].label = "Dirección"
