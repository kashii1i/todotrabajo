from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.cuentas.models import Usuario
from apps.publicaciones.models import Categoria, Publicacion
from apps.ubicaciones.models import Comuna
from .models import Conversacion, Mensaje


class ChatTests(TestCase):
    def setUp(self):
        self.autor = Usuario.objects.create_user("autor@test.cl", "clave-segura-123")
        self.interesado = Usuario.objects.create_user("interesado@test.cl", "clave-segura-123")
        self.intruso = Usuario.objects.create_user("intruso@test.cl", "clave-segura-123")
        self.pub = Publicacion.objects.create(
            autor=self.autor,
            tipo=Publicacion.Tipo.OFERTA,
            titulo="Gasfiter a domicilio",
            descripcion="Arreglo fugas y calefont",
            categoria=Categoria.objects.get(slug="gasfiteria"),
            comuna=Comuna.objects.get(nombre="Ñuñoa"),
        )

    def test_conversacion_y_mensajes(self):
        conv = Conversacion.objects.create(publicacion=self.pub, interesado=self.interesado)
        Mensaje.objects.create(conversacion=conv, autor=self.interesado, texto="Hola, ¿disponible?")
        Mensaje.objects.create(conversacion=conv, autor=self.autor, texto="Sí, mañana.")
        self.assertEqual(conv.mensajes.count(), 2)
        self.assertIn(conv, Conversacion.para_usuario(self.autor))
        self.assertIn(conv, Conversacion.para_usuario(self.interesado))
        self.assertNotIn(conv, Conversacion.para_usuario(self.intruso))

    def test_no_se_puede_conversar_con_uno_mismo(self):
        conv = Conversacion(publicacion=self.pub, interesado=self.autor)
        with self.assertRaises(ValidationError):
            conv.full_clean()

    def test_intruso_no_puede_escribir(self):
        conv = Conversacion.objects.create(publicacion=self.pub, interesado=self.interesado)
        with self.assertRaises(ValidationError):
            Mensaje(conversacion=conv, autor=self.intruso, texto="spam").full_clean()

    def test_una_conversacion_por_interesado(self):
        Conversacion.objects.create(publicacion=self.pub, interesado=self.interesado)
        with self.assertRaises(IntegrityError):
            Conversacion.objects.create(publicacion=self.pub, interesado=self.interesado)
