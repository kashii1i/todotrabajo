from django.test import TestCase

from .models import Perfil, Usuario


class UsuarioTests(TestCase):
    def test_crear_usuario_con_email(self):
        u = Usuario.objects.create_user("ana@test.cl", "clave-segura-123")
        self.assertEqual(u.email, "ana@test.cl")
        self.assertTrue(u.check_password("clave-segura-123"))
        self.assertFalse(u.is_staff)

    def test_perfil_se_crea_automaticamente(self):
        u = Usuario.objects.create_user("beto@test.cl", "clave-segura-123")
        self.assertTrue(Perfil.objects.filter(usuario=u).exists())

    def test_superusuario(self):
        u = Usuario.objects.create_superuser("admin@test.cl", "clave-segura-123")
        self.assertTrue(u.is_staff and u.is_superuser)
