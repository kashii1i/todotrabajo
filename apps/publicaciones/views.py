from django.shortcuts import render

from .models import Categoria, Publicacion


def inicio(request):
    contexto = {
        "categorias": Categoria.objects.filter(padre__isnull=True).prefetch_related("subcategorias"),
        "ultimas": Publicacion.objects.filter(estado=Publicacion.Estado.ACTIVA)
        .select_related("categoria", "comuna", "comuna__region")[:8],
    }
    return render(request, "publicaciones/inicio.html", contexto)
