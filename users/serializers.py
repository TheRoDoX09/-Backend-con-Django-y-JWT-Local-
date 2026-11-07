from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'telefono', 'password', 'is_active', 'is_staff']
        # write_only: la contraseña se recibe, pero nunca aparece en una respuesta.
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def update(self, instance, validated_data):
        # La contraseña solo cambia si viene en la petición (PUT y PATCH).
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserCreateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
