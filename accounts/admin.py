# admin.py (accounts)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Department, Role, Client

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'department', 'role', 'is_staff', 'is_active',]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('department', 'role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Client)  # Registre o modelo Client
