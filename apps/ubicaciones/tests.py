from django.test import TestCase

from .models import Comuna, Region


class DatosInicialesTests(TestCase):
    def test_regiones_y_comunas_cargadas(self):
        self.assertEqual(Region.objects.count(), 16)
        self.assertEqual(Comuna.objects.count(), 346)
        self.assertEqual(Region.objects.get(codigo="RM").comunas.count(), 52)
        self.assertEqual(Region.objects.first().codigo, "XV")  # orden norte → sur
