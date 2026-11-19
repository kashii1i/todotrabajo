from django import forms
from django.db.models import F
from django.db.models.functions import Coalesce

from apps.ubicaciones.forms import RegionComunaMixin
from apps.ubicaciones.models import Comuna
from .models import Categoria, Publicacion


class CategoriaChoiceField(forms.ModelChoiceField):
    """Muestra las subcategorías indentadas bajo su categoría padre."""

    def __init__(self, **kwargs):
        queryset = Categoria.objects.order_by(
            Coalesce("padre__orden", "orden"), F("padre").asc(nulls_first=True), "orden"
        )
        super().__init__(queryset=queryset, **kwargs)

    def label_from_instance(self, obj):
        return f"— {obj.nombre}" if obj.padre_id else obj.nombre


class FiltroPublicacionesForm(RegionComunaMixin, forms.Form):
    """Filtros del listado. Todos opcionales."""

    texto_vacio_comuna = "Todas las comunas"

    q = forms.CharField(
        label="Buscar", required=False, max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "¿Qué necesitas? Ej: gasfiter, clases de inglés"}),
    )
    tipo = forms.ChoiceField(
        label="Tipo", required=False,
        choices=[("", "Ofertas y encargos")] + Publicacion.Tipo.choices,
    )
    categoria = CategoriaChoiceField(label="Categoría", required=False, empty_label="Todas las categorías")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.none(), required=False, label="Comuna")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["region"].empty_label = "Todo Chile"


class PublicacionForm(RegionComunaMixin, forms.ModelForm):
    """Formulario para crear y editar publicaciones (lo usan las vistas de crear/editar)."""

    categoria = CategoriaChoiceField(label="Categoría", empty_label="Selecciona una categoría")

    class Meta:
        model = Publicacion
        fields = ["tipo", "titulo", "descripcion", "categoria", "comuna", "modalidad_precio", "precio"]
        widgets = {
            "tipo": forms.RadioSelect,
            "descripcion": forms.Textarea(attrs={"rows": 5}),
            "precio": forms.NumberInput(attrs={"min": 0, "step": 500, "placeholder": "Ej: 25000"}),
        }

    def clean(self):
        datos = super().clean()
        if datos.get("modalidad_precio") != Publicacion.ModalidadPrecio.A_CONVENIR and not datos.get("precio"):
            self.add_error("precio", "Indica un precio, o elige «A convenir».")
        return datos
