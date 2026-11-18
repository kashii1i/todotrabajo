from django.contrib import admin

from .models import Comuna, Region


class ComunaInline(admin.TabularInline):
    model = Comuna
    extra = 0


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["nombre", "codigo", "orden"]
    inlines = [ComunaInline]


@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "region"]
    list_filter = ["region"]
    search_fields = ["nombre"]
