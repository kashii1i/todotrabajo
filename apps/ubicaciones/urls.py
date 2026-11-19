from django.urls import path

from . import views

app_name = "ubicaciones"

urlpatterns = [
    path("comunas/", views.comunas_por_region, name="comunas"),
]
