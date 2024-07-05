from django.urls import path
from .views import login_view, logout_view, homepage_view, list_clients, delete_client, edit_client, add_client, list_users, add_user, edit_user, delete_user, keep_session_alive

urlpatterns = [
    path("", login_view, name="login"),
    # path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('homepage/', homepage_view, name='homepage'),
    path('users/', list_users, name='list_users'),
    path('users/add/', add_user, name='add_user'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('clients/', list_clients, name='list_clients'),
    path('clients/add/', add_client, name='add_client'),
    path('clients/edit/<int:client_id>/', edit_client, name='edit_client'),
    path('clients/delete/<int:client_id>/', delete_client, name='delete_client'),
    path('keep-session-alive/', keep_session_alive, name='keep_session_alive'),

]

