from django.contrib import admin
from .models import CustomUser, Department, Role, Client

# Função que será chamada para aprovar os usuários selecionados
def approve_users(modeladmin, request, queryset):
    queryset.update(is_approved=True)  # Atualiza todos os usuários selecionados
    modeladmin.message_user(request, f"{queryset.count()} usuários foram aprovados com sucesso.")

approve_users.short_description = "Aprovar usuários selecionados"

# Admin para CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'department', 'role', 'is_approved')
    list_filter = ('department', 'role', 'is_approved')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    actions = [approve_users]  # Adiciona a ação personalizada

# Admin para Department e Role (opcional, mas útil para organização)
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_type')

# Admin para Client
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'responsible')

