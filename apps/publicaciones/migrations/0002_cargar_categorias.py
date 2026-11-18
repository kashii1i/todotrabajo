from django.db import migrations

from apps.publicaciones.datos import CATEGORIAS


def cargar(apps, schema_editor):
    Categoria = apps.get_model("publicaciones", "Categoria")
    for orden, (nombre, slug, subs) in enumerate(CATEGORIAS, start=1):
        padre, _ = Categoria.objects.update_or_create(
            slug=slug, defaults={"nombre": nombre, "orden": orden}
        )
        for sub_orden, (sub_nombre, sub_slug) in enumerate(subs, start=1):
            Categoria.objects.update_or_create(
                slug=sub_slug, defaults={"nombre": sub_nombre, "padre": padre, "orden": sub_orden}
            )


def descargar(apps, schema_editor):
    Categoria = apps.get_model("publicaciones", "Categoria")
    Categoria.objects.filter(padre__isnull=False).delete()
    Categoria.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("publicaciones", "0001_initial")]
    operations = [migrations.RunPython(cargar, descargar)]
