from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.publicaciones.views import inicio

admin.site.site_header = "TodoTrabajo · Administración"
admin.site.site_title = "TodoTrabajo"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", inicio, name="inicio"),
    path("cuentas/", include("apps.cuentas.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
