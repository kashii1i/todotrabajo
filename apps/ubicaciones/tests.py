from django import forms
from django.test import TestCase
from django.urls import reverse

from .forms import RegionComunaMixin
from .models import Comuna, Region


class DatosInicialesTests(TestCase):
    def test_regiones_y_comunas_cargadas(self):
        self.assertEqual(Region.objects.count(), 16)
        self.assertEqual(Comuna.objects.count(), 346)
        self.assertEqual(Region.objects.get(codigo="RM").comunas.count(), 52)
        self.assertEqual(Region.objects.first().codigo, "XV")  # orden norte → sur


class ComunasPorRegionTests(TestCase):
    def test_devuelve_solo_comunas_de_la_region(self):
        rm = Region.objects.get(codigo="RM")
        r = self.client.get(reverse("ubicaciones:comunas"), {"region": rm.pk})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Ñuñoa")
        self.assertNotContains(r, "Valdivia")
        self.assertEqual(r.content.decode().count("<option"), 52 + 1)  # + opción vacía

    def test_region_invalida_devuelve_solo_opcion_vacia(self):
        r = self.client.get(reverse("ubicaciones:comunas"), {"region": "abc"})
        self.assertEqual(r.content.decode().count("<option"), 1)


class FormPrueba(RegionComunaMixin, forms.Form):
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.none())


class RegionComunaMixinTests(TestCase):
    def setUp(self):
        self.rm = Region.objects.get(codigo="RM")
        self.nunoa = Comuna.objects.get(nombre="Ñuñoa")
        self.valdivia = Comuna.objects.get(nombre="Valdivia")

    def test_sin_region_no_ofrece_comunas(self):
        self.assertEqual(FormPrueba().fields["comuna"].queryset.count(), 0)

    def test_region_va_antes_de_comuna(self):
        self.assertEqual(list(FormPrueba().fields), ["region", "comuna"])

    def test_comuna_valida(self):
        form = FormPrueba({"region": self.rm.pk, "comuna": self.nunoa.pk})
        self.assertTrue(form.is_valid(), form.errors)

    def test_comuna_de_otra_region_es_rechazada(self):
        form = FormPrueba({"region": self.rm.pk, "comuna": self.valdivia.pk})
        self.assertFalse(form.is_valid())
        self.assertIn("comuna", form.errors)

    def test_trae_atributos_htmx(self):
        html = str(FormPrueba()["region"])
        self.assertIn("hx-get", html)
        self.assertIn('hx-target="#id_comuna"', html)
