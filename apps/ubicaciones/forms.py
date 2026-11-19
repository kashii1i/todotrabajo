from urllib.parse import quote

from django import forms
from django.urls import reverse

from .models import Comuna, Region


class RegionComunaMixin:
    """Agrega un selector de región que filtra las comunas con HTMX.

    Uso: heredar ANTES de forms.Form / forms.ModelForm en cualquier formulario
    que tenga un campo `comuna`:

        class MiForm(RegionComunaMixin, forms.ModelForm): ...

    - Crea el campo `region` (no se guarda en el modelo; solo sirve para filtrar).
    - El campo `comuna` solo ofrece las comunas de la región elegida.
    - Valida que la comuna pertenezca a la región.
    """

    texto_vacio_comuna = "Selecciona una comuna"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        comuna_field = self.fields["comuna"]

        self.fields["region"] = forms.ModelChoiceField(
            queryset=Region.objects.all(),
            required=comuna_field.required,
            label="Región",
            empty_label="Selecciona una región",
        )
        self._mover_region_antes_de_comuna()

        region_id = self._region_inicial()
        if region_id:
            self.initial.setdefault("region", region_id)
        comuna_field.queryset = (
            Comuna.objects.filter(region_id=region_id) if region_id else Comuna.objects.none()
        )
        comuna_field.empty_label = self.texto_vacio_comuna

        # Al cambiar la región, HTMX pide las comunas y reemplaza las opciones del <select>.
        self.fields["region"].widget.attrs.update({
            "hx-get": f"{reverse('ubicaciones:comunas')}?vacio={quote(self.texto_vacio_comuna)}",
            "hx-target": f"#{self['comuna'].auto_id}",
            "hx-trigger": "change",
            "hx-swap": "innerHTML",
        })

    def _region_inicial(self):
        """Región desde: datos enviados → initial → comuna de la instancia."""
        if self.is_bound:
            valor = self.data.get(self.add_prefix("region"))
        else:
            valor = self.initial.get("region")
            instancia = getattr(self, "instance", None)
            if not valor and instancia is not None and getattr(instancia, "comuna_id", None):
                valor = instancia.comuna.region_id
        if isinstance(valor, Region):
            return valor.pk
        try:
            return int(valor) if valor else None
        except (TypeError, ValueError):
            return None

    def _mover_region_antes_de_comuna(self):
        campos = list(self.fields.items())
        region = self.fields.pop("region")
        nuevos = {}
        for nombre, campo in campos:
            if nombre == "region":
                continue
            if nombre == "comuna":
                nuevos["region"] = region
            nuevos[nombre] = campo
        self.fields = nuevos

    def clean(self):
        datos = super().clean()
        region, comuna = datos.get("region"), datos.get("comuna")
        if region and comuna and comuna.region_id != region.pk:
            self.add_error("comuna", "La comuna no pertenece a la región seleccionada.")
        return datos
