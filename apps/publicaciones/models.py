from django.conf import settings
from django.db import models


class Categoria(models.Model):
    """Categoría de servicio. Admite un nivel de subcategorías vía `padre`."""

    nombre = models.CharField(max_length=80)
    slug = models.SlugField(max_length=90, unique=True)
    padre = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategorias",
    )
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["orden", "nombre"]

    def __str__(self):
        return f"{self.padre} › {self.nombre}" if self.padre_id else self.nombre


class Publicacion(models.Model):
    class Tipo(models.TextChoices):
        OFERTA = "oferta", "Ofrezco un servicio"
        ENCARGO = "encargo", "Busco quien lo haga"

    class ModalidadPrecio(models.TextChoices):
        FIJO = "fijo", "Precio fijo"
        POR_HORA = "hora", "Por hora"
        A_CONVENIR = "convenir", "A convenir"

    class Estado(models.TextChoices):
        ACTIVA = "activa", "Activa"
        PAUSADA = "pausada", "Pausada"
        CERRADA = "cerrada", "Cerrada"

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="publicaciones"
    )
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    titulo = models.CharField("título", max_length=120)
    descripcion = models.TextField("descripción")
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="publicaciones"
    )
    comuna = models.ForeignKey(
        "ubicaciones.Comuna", on_delete=models.PROTECT, related_name="publicaciones"
    )
    modalidad_precio = models.CharField(
        max_length=10, choices=ModalidadPrecio.choices, default=ModalidadPrecio.A_CONVENIR
    )
    precio = models.PositiveIntegerField(
        "precio (CLP)", null=True, blank=True, help_text="En pesos chilenos, sin decimales"
    )
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ACTIVA)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "publicación"
        verbose_name_plural = "publicaciones"
        ordering = ["-creado"]
        indexes = [
            models.Index(fields=["tipo", "estado", "-creado"]),
            models.Index(fields=["categoria", "estado"]),
            models.Index(fields=["comuna", "estado"]),
        ]
        constraints = [
            # Si el precio no es "a convenir", debe venir un monto.
            models.CheckConstraint(
                condition=models.Q(modalidad_precio="convenir") | models.Q(precio__isnull=False),
                name="precio_requerido_si_no_es_a_convenir",
            )
        ]

    def __str__(self):
        return self.titulo
