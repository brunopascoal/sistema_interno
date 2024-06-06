from django.urls import path
from .views import register_view, login_view, logout_view, homepage_view

urlpatterns = [
    path("", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('homepage/', homepage_view, name='homepage'),  # Assumindo que você tenha uma view chamada homepage_view

]
