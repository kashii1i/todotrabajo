from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from apps.cuentas.models import Usuario
from apps.ubicaciones.models import Comuna
from .forms import PublicacionForm
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


class ListadoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.autor = Usuario.objects.create_user("autor@test.cl", "clave-segura-123")
        cls.nunoa = Comuna.objects.get(nombre="Ñuñoa")
        cls.maipu = Comuna.objects.get(nombre="Maipú")
        cls.valdivia = Comuna.objects.get(nombre="Valdivia")
        cls.gasfiteria = Categoria.objects.get(slug="gasfiteria")
        cls.idiomas = Categoria.objects.get(slug="clases-idiomas")

        def pub(titulo, **extra):
            datos = dict(autor=cls.autor, tipo="oferta", descripcion="...",
                         categoria=cls.gasfiteria, comuna=cls.nunoa)
            datos.update(extra)
            return Publicacion.objects.create(titulo=titulo, **datos)

        pub("Gasfiter Ñuñoa")
        pub("Gasfiter Maipú", comuna=cls.maipu)
        pub("Busco gasfiter en Valdivia", tipo="encargo", comuna=cls.valdivia)
        pub("Clases de inglés", categoria=cls.idiomas, descripcion="Nivel conversacional")
        pub("Publicación pausada", estado="pausada")

    def get(self, **params):
        return self.client.get(reverse("publicaciones:listado"), params)

    def titulos(self, respuesta):
        return {p.titulo for p in respuesta.context["pagina"]}

    def test_sin_filtros_muestra_solo_activas(self):
        r = self.get()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(self.titulos(r)), 4)
        self.assertNotIn("Publicación pausada", self.titulos(r))

    def test_filtro_tipo(self):
        self.assertEqual(self.titulos(self.get(tipo="encargo")), {"Busco gasfiter en Valdivia"})

    def test_busqueda_en_titulo_y_descripcion(self):
        self.assertEqual(self.titulos(self.get(q="conversacional")), {"Clases de inglés"})
        self.assertEqual(len(self.titulos(self.get(q="GASFITER"))), 3)

    def test_categoria_padre_incluye_subcategorias(self):
        padre = self.idiomas.padre
        self.assertEqual(self.titulos(self.get(categoria=padre.pk)), {"Clases de inglés"})

    def test_filtro_region_y_comuna(self):
        rm = self.nunoa.region
        self.assertEqual(len(self.titulos(self.get(region=rm.pk))), 3)
        self.assertEqual(
            self.titulos(self.get(region=rm.pk, comuna=self.maipu.pk)), {"Gasfiter Maipú"}
        )

    def test_comuna_de_otra_region_se_ignora(self):
        # Pasa al cambiar la región en el filtro: la comuna anterior queda obsoleta.
        r = self.get(region=self.nunoa.region.pk, comuna=self.valdivia.pk)
        self.assertEqual(len(self.titulos(r)), 3)

    def test_peticion_htmx_devuelve_solo_resultados(self):
        r = self.client.get(reverse("publicaciones:listado"), HTTP_HX_REQUEST="true")
        self.assertTemplateUsed(r, "publicaciones/parciales/_resultados.html")
        self.assertTemplateNotUsed(r, "base.html")

    def test_paginacion_mantiene_filtros(self):
        for i in range(15):
            Publicacion.objects.create(
                autor=self.autor, tipo="encargo", titulo=f"Encargo {i}", descripcion="...",
                categoria=self.gasfiteria, comuna=self.nunoa,
            )
        r = self.get(tipo="encargo")
        self.assertEqual(len(r.context["pagina"]), 12)
        self.assertContains(r, "tipo=encargo&page=2")
        self.assertEqual(len(self.get(tipo="encargo", page=2).context["pagina"]), 4)


class FiltroClpTests(TestCase):
    def test_formato_pesos_chilenos(self):
        from .templatetags.formato import clp
        self.assertEqual(clp(25000), "$25.000")
        self.assertEqual(clp(1500000), "$1.500.000")
        self.assertEqual(clp(None), "")


class PublicacionFormTests(TestCase):
    def setUp(self):
        self.nunoa = Comuna.objects.get(nombre="Ñuñoa")
        self.datos = {
            "tipo": "oferta", "titulo": "Gasfiter", "descripcion": "Arreglo calefont",
            "categoria": Categoria.objects.get(slug="gasfiteria").pk,
            "region": self.nunoa.region_id, "comuna": self.nunoa.pk,
            "modalidad_precio": "fijo", "precio": "",
        }

    def test_precio_fijo_sin_monto_da_error_amigable(self):
        form = PublicacionForm(self.datos)
        self.assertFalse(form.is_valid())
        self.assertIn("precio", form.errors)

    def test_a_convenir_sin_monto_es_valido(self):
        form = PublicacionForm({**self.datos, "modalidad_precio": "convenir"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_editar_precarga_region_desde_la_comuna(self):
        pub = Publicacion(comuna=self.nunoa)
        form = PublicacionForm(instance=pub)
        self.assertEqual(form.initial["region"], self.nunoa.region_id)
        self.assertIn(self.nunoa, form.fields["comuna"].queryset)
