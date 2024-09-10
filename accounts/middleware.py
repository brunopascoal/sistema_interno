from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse

class SessionExpiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Logando o caminho acessado
        print(f"Path acessado: {request.path}")

        # URLs permitidas para usuários não autenticados
        allowed_urls = [settings.LOGIN_URL, reverse('register'), '/favicon.ico']
        print(f"Allowed URLs: {allowed_urls}")  # Para ver os caminhos completos

        # Adicionando exceções para /favicon.ico e outras requisições estáticas
        if not request.user.is_authenticated and request.path not in allowed_urls and not request.path.startswith('/static/'):
            return redirect(settings.LOGIN_URL)

        response = self.get_response(request)
        return response
