from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Conversacion(models.Model):
    """Conversación entre el autor de una publicación y un usuario interesado.

    Hay a lo más una conversación por (publicación, interesado).
    El otro participante siempre es `publicacion.autor`.
    """

    publicacion = models.ForeignKey(
        "publicaciones.Publicacion", on_delete=models.CASCADE, related_name="conversaciones"
    )
    interesado = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversaciones_iniciadas"
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)  # se toca con cada mensaje nuevo

    class Meta:
        verbose_name = "conversación"
        verbose_name_plural = "conversaciones"
        ordering = ["-actualizado"]
        constraints = [
            models.UniqueConstraint(
                fields=["publicacion", "interesado"], name="una_conversacion_por_interesado"
            )
        ]

    def __str__(self):
        return f"{self.interesado} ↔ {self.publicacion.autor} · {self.publicacion}"

    @property
    def participantes(self):
        return [self.publicacion.autor, self.interesado]

    def participa(self, usuario):
        return usuario.pk in (self.publicacion.autor_id, self.interesado_id)

    def clean(self):
        if self.publicacion_id and self.interesado_id == self.publicacion.autor_id:
            raise ValidationError("No puedes iniciar una conversación sobre tu propia publicación.")

    @classmethod
    def para_usuario(cls, usuario):
        """Todas las conversaciones donde participa `usuario`."""
        return cls.objects.filter(
            models.Q(interesado=usuario) | models.Q(publicacion__autor=usuario)
        ).select_related("publicacion", "publicacion__autor", "interesado")


class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name="mensajes")
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mensajes_enviados"
    )
    texto = models.TextField(max_length=2000)
    leido = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "mensaje"
        verbose_name_plural = "mensajes"
        ordering = ["creado"]
        indexes = [models.Index(fields=["conversacion", "creado"])]

    def __str__(self):
        return f"{self.autor}: {self.texto[:40]}"

    def clean(self):
        if self.conversacion_id and self.autor_id and not self.conversacion.participa(self.autor):
            raise ValidationError("Solo los participantes pueden escribir en esta conversación.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Sube la conversación al tope de la bandeja.
        Conversacion.objects.filter(pk=self.conversacion_id).update(actualizado=self.creado)
