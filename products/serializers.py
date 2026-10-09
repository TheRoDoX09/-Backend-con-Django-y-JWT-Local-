from rest_framework import serializers
from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category']
        #fields = '__all__'

    def to_representation(self, instance):
        # Recibe el id de la categoría, pero al responder muestra su nombre
        data = super().to_representation(instance)
        data['category'] = str(instance.category)
        return data
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'