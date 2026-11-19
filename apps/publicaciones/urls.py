
from django.urls import path

from . import views

app_name = "publicaciones"

urlpatterns = [
    path("", views.listado, name="listado"),
    path("nueva/", views.crear, name="crear"),
    path("<int:pk>/", views.detalle, name="detalle"),

    # TODO (Sprint 3):
    # path("<int:pk>/editar/", views.editar, name="editar"),
    # path("<int:pk>/estado/", views.cambiar_estado, name="cambiar_estado"),
    # path("mias/", views.mis_publicaciones, name="mias"),
]
