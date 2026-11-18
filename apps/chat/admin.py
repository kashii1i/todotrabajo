from django.contrib import admin

from .models import Conversacion, Mensaje


class MensajeInline(admin.TabularInline):
    model = Mensaje
    extra = 0
    readonly_fields = ["autor", "texto", "leido", "creado"]


@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ["publicacion", "interesado", "creado", "actualizado"]
    search_fields = ["publicacion__titulo", "interesado__email"]
    raw_id_fields = ["publicacion", "interesado"]
    inlines = [MensajeInline]
