from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Category, Product

User = get_user_model()


class CategoriaAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.usuario = User.objects.create_user(username='cliente_tienda', email='cliente@tienda.com', password='tienda2026')
        self.client.force_authenticate(user=self.usuario)
        self.categoria_hogar = Category.objects.create(name='Hogar')

    def test_crear_categoria_electronica(self):
        respuesta = self.client.post('/api/categories/', {'name': 'Electrónica'})
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)
        self.assertTrue(Category.objects.filter(name='Electrónica').exists())

    def test_listar_categorias(self):
        respuesta = self.client.get('/api/categories/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.data), 1)
        self.assertEqual(respuesta.data[0]['name'], 'Hogar')


class ProductoAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.usuario = User.objects.create_user(username='cliente_tienda', email='cliente@tienda.com', password='tienda2026')
        self.client.force_authenticate(user=self.usuario)
        self.categoria_ropa = Category.objects.create(name='Ropa')
        self.camiseta = Product.objects.create(
            name='Camiseta básica',
            category=self.categoria_ropa,
            description='Camiseta de algodón 100%',
            price=15.00
        )

    def test_crear_producto_pantalon(self):
        respuesta = self.client.post('/api/products/', {
            'name': 'Pantalón jeans',
            'category': self.categoria_ropa.id,
            'description': 'Jeans corte recto',
            'price': 35.50
        })
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(respuesta.data['category'], 'Ropa')

    def test_listar_productos(self):
        respuesta = self.client.get('/api/products/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.data), 1)
        self.assertEqual(respuesta.data[0]['name'], 'Camiseta básica')

    def test_actualizar_precio_camiseta(self):
        respuesta = self.client.put(f'/api/products/{self.camiseta.id}/', {
            'name': 'Camiseta básica oversize',
            'category': self.categoria_ropa.id,
            'description': 'Camiseta de algodón 100%, corte oversize',
            'price': 19.99
        })
        self.assertEqual(respuesta.status_code, 200)
        self.camiseta.refresh_from_db()
        self.assertEqual(self.camiseta.name, 'Camiseta básica oversize')
        self.assertEqual(str(self.camiseta.price), '19.99')

    def test_eliminar_camiseta(self):
        respuesta = self.client.delete(f'/api/products/{self.camiseta.id}/')
        self.assertEqual(respuesta.status_code, 204)
        self.assertFalse(Product.objects.filter(id=self.camiseta.id).exists())

    def test_precio_final_autenticado(self):
        response = self.client.get(f'/api/products/{self.camiseta.id}/precio-final/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('precio_final', response.data)

    def test_precio_final_sin_autenticar(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/products/{self.camiseta.id}/precio-final/')
        self.assertEqual(response.status_code, 401)
