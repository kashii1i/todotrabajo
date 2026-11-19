from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .forms import FiltroPublicacionesForm
from .models import Categoria, Publicacion

POR_PAGINA = 12


def inicio(request):
    contexto = {
        "categorias": Categoria.objects.filter(padre__isnull=True).prefetch_related("subcategorias"),
        "ultimas": Publicacion.objects.filter(estado=Publicacion.Estado.ACTIVA)
        .select_related("categoria", "comuna", "comuna__region")[:8],
    }
    return render(request, "publicaciones/inicio.html", contexto)


def filtrar_publicaciones(datos):
    """Aplica los filtros (cleaned_data del FiltroPublicacionesForm) a las publicaciones activas."""
    qs = Publicacion.objects.filter(estado=Publicacion.Estado.ACTIVA).select_related(
        "categoria", "categoria__padre", "comuna", "comuna__region", "autor"
    )
    if q := datos.get("q"):
        qs = qs.filter(Q(titulo__icontains=q) | Q(descripcion__icontains=q))
    if tipo := datos.get("tipo"):
        qs = qs.filter(tipo=tipo)
    if categoria := datos.get("categoria"):
        # Una categoría padre incluye todas sus subcategorías.
        qs = qs.filter(Q(categoria=categoria) | Q(categoria__padre=categoria))
    if comuna := datos.get("comuna"):
        qs = qs.filter(comuna=comuna)
    elif region := datos.get("region"):
        qs = qs.filter(comuna__region=region)
    return qs


def listado(request):
    form = FiltroPublicacionesForm(request.GET or None)
    datos = {}
    if form.is_bound:
        # Si un filtro viene inválido (p. ej. una comuna de otra región tras cambiar la región),
        # cleaned_data solo conserva los campos válidos: se ignora ese filtro y se aplican los demás.
        form.is_valid()
        datos = form.cleaned_data

    pagina = Paginator(filtrar_publicaciones(datos), POR_PAGINA).get_page(request.GET.get("page"))

    parametros = request.GET.copy()
    parametros.pop("page", None)

    contexto = {"form": form, "pagina": pagina, "parametros": parametros.urlencode()}
    plantilla = "publicaciones/parciales/_resultados.html" if request.htmx else "publicaciones/listado.html"
    return render(request, plantilla, contexto)
