from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


# Se usa UserAdmin en lugar de admin.site.register(User) como en el manual:
# el admin genérico guarda en texto plano la contraseña de los usuarios nuevos.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'email', 'username', 'telefono', 'is_active', 'is_staff']
    ordering = ['email']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Datos de contacto', {'fields': ('telefono',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Datos de contacto', {'fields': ('email', 'telefono')}),
    )
