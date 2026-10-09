from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
      
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='get_products', verbose_name='Categoría', default=1)
    description = models.TextField(verbose_name='Descripción')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    is_active = models.BooleanField(default=True,)


    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def crear_con_categoria_default(cls, name, description, price):
        # Factory Method: encapsula cómo se construye un Product. Si no se indica
        # categoría, se asigna (o se crea) la categoría por defecto 'Sin categoría'.
        categoria_default, _ = Category.objects.get_or_create(name='Sin categoría')
        return cls.objects.create(
            name=name,
            description=description,
            price=price,
            category=categoria_default
        )
