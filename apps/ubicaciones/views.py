from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Comuna


@require_GET
def comunas_por_region(request):
    """Devuelve las <option> de las comunas de una región (para HTMX)."""
    region_id = request.GET.get("region")
    comunas = Comuna.objects.filter(region_id=region_id) if region_id and region_id.isdigit() else []
    vacio = request.GET.get("vacio", "Selecciona una comuna")[:40]
    return render(request, "ubicaciones/_opciones_comunas.html", {"comunas": comunas, "vacio": vacio})
