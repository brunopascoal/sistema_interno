from django.urls import path
from .views import register_view, login_view, logout_view, homepage_view, list_clients, delete_client, edit_client

urlpatterns = [
    path("", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('homepage/', homepage_view, name='homepage'),
    path('clients/', list_clients, name='list_clients'),
    path('clients/edit/<int:client_id>/', edit_client, name='edit_client'),
    path('clients/delete/<int:client_id>/', delete_client, name='delete_client'),
]

