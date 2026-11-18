from django.db import models


class Region(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField("código", max_length=5, unique=True)  # XV, I, II, ..., RM
    orden = models.PositiveSmallIntegerField(help_text="Orden geográfico de norte a sur")

    class Meta:
        verbose_name = "región"
        verbose_name_plural = "regiones"
        ordering = ["orden"]

    def __str__(self):
        return self.nombre


class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="comunas")

    class Meta:
        verbose_name = "comuna"
        verbose_name_plural = "comunas"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(fields=["region", "nombre"], name="comuna_unica_por_region")
        ]

    def __str__(self):
        return self.nombre
