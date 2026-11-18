from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from apps.cuentas.models import Usuario
from apps.ubicaciones.models import Comuna
from .models import Categoria, Publicacion


class PublicacionTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user("pia@test.cl", "clave-segura-123")
        self.cat = Categoria.objects.get(slug="clases-matematicas")
        self.comuna = Comuna.objects.get(nombre="Valdivia")

    def test_categorias_cargadas(self):
        self.assertTrue(Categoria.objects.filter(padre__isnull=True).count() >= 10)
        self.assertEqual(self.cat.padre.slug, "clases")

    def test_precio_obligatorio_si_es_fijo(self):
        with self.assertRaises(IntegrityError):
            Publicacion.objects.create(
                autor=self.usuario, tipo="oferta", titulo="Clases", descripcion="...",
                categoria=self.cat, comuna=self.comuna, modalidad_precio="fijo",
            )

    def test_inicio_muestra_publicacion(self):
        Publicacion.objects.create(
            autor=self.usuario, tipo="encargo", titulo="Busco profe de cálculo",
            descripcion="Para 1er año", categoria=self.cat, comuna=self.comuna,
        )
        r = self.client.get(reverse("inicio"))
        self.assertContains(r, "Busco profe de cálculo")
        self.assertContains(r, "Clases particulares")
