from django.db import migrations

# Los datos viven en apps/ubicaciones/datos.py. Si cambian, crear una migración nueva en vez de editar esta.
from apps.ubicaciones.datos import REGIONES


def cargar(apps, schema_editor):
    Region = apps.get_model("ubicaciones", "Region")
    Comuna = apps.get_model("ubicaciones", "Comuna")
    for orden, (codigo, nombre, comunas) in enumerate(REGIONES, start=1):
        region, _ = Region.objects.update_or_create(
            codigo=codigo, defaults={"nombre": nombre, "orden": orden}
        )
        for comuna in comunas:
            Comuna.objects.get_or_create(region=region, nombre=comuna)


def descargar(apps, schema_editor):
    apps.get_model("ubicaciones", "Comuna").objects.all().delete()
    apps.get_model("ubicaciones", "Region").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("ubicaciones", "0001_initial")]
    operations = [migrations.RunPython(cargar, descargar)]
