from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

User = get_user_model()


class UsuarioAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin_tienda', email='admin@tienda.com', password='admin2026'
        )
        self.cliente = User.objects.create_user(
            username='cliente', email='cliente@tienda.com', password='cliente2026', telefono='6641234567'
        )
        self.client.force_authenticate(user=self.admin)
        self.url_cliente = f'/api/v1/users/{self.cliente.id}/'

    def test_crear_usuario_guarda_hash_y_no_lo_devuelve(self):
        respuesta = self.client.post('/api/v1/users/', {
            'username': 'nuevo', 'email': 'nuevo@tienda.com', 'password': 'nuevo2026', 'telefono': '6640000000'
        })
        self.assertEqual(respuesta.status_code, 201)
        self.assertNotIn('password', respuesta.data)
        self.assertEqual(respuesta.data['telefono'], '6640000000')
        self.assertTrue(User.objects.get(username='nuevo').check_password('nuevo2026'))

    def test_crear_usuario_sin_password_es_400(self):
        respuesta = self.client.post('/api/v1/users/', {'username': 'nuevo', 'email': 'nuevo@tienda.com'})
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn('password', respuesta.data)

    def test_listado_y_detalle_no_incluyen_password(self):
        self.assertNotIn('password', self.client.get('/api/v1/users/').data[0])
        self.assertNotIn('password', self.client.get(self.url_cliente).data)

    def test_me_devuelve_datos_propios_sin_password(self):
        self.client.force_authenticate(user=self.cliente)
        respuesta = self.client.get('/api/v1/auth/me/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data['email'], 'cliente@tienda.com')
        self.assertEqual(respuesta.data['telefono'], '6641234567')
        self.assertNotIn('password', respuesta.data)

    def test_me_sin_token_es_401(self):
        self.client.force_authenticate(user=None)
        self.assertEqual(self.client.get('/api/v1/auth/me/').status_code, 401)

    def test_patch_sin_password_no_la_cambia(self):
        hash_original = self.cliente.password
        respuesta = self.client.patch(self.url_cliente, {'telefono': '6649999999'})
        self.assertEqual(respuesta.status_code, 200)
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.telefono, '6649999999')
        self.assertEqual(self.cliente.password, hash_original)

    def test_put_sin_password_no_la_cambia(self):
        hash_original = self.cliente.password
        respuesta = self.client.put(self.url_cliente, {'username': 'cliente', 'email': 'cliente@tienda.com'})
        self.assertEqual(respuesta.status_code, 200)
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.password, hash_original)

    def test_patch_y_put_con_password_guardan_hash(self):
        self.client.patch(self.url_cliente, {'password': 'cambiada2026'})
        self.cliente.refresh_from_db()
        self.assertTrue(self.cliente.check_password('cambiada2026'))
        self.client.put(self.url_cliente, {
            'username': 'cliente', 'email': 'cliente@tienda.com', 'password': 'otra2026'
        })
        self.cliente.refresh_from_db()
        self.assertTrue(self.cliente.check_password('otra2026'))

    def test_login_jwt_con_email(self):
        self.client.force_authenticate(user=None)
        respuesta = self.client.post('/api/v1/auth/token/', {
            'email': 'cliente@tienda.com', 'password': 'cliente2026'
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('access', respuesta.data)

    def test_usuario_normal_no_accede_al_crud(self):
        self.client.force_authenticate(user=self.cliente)
        self.assertEqual(self.client.get('/api/v1/users/').status_code, 403)
