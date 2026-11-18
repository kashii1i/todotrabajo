from django.contrib import admin

from .models import Categoria, Publicacion


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "padre", "slug", "orden"]
    list_filter = ["padre"]
    search_fields = ["nombre"]
    prepopulated_fields = {"slug": ["nombre"]}


@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ["titulo", "tipo", "categoria", "comuna", "precio", "estado", "autor", "creado"]
    list_filter = ["tipo", "estado", "categoria", "comuna__region"]
    search_fields = ["titulo", "descripcion", "autor__email"]
    autocomplete_fields = ["autor", "categoria", "comuna"]
    date_hierarchy = "creado"
