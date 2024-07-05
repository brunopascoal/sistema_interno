# middleware.py

from django.shortcuts import redirect
from django.conf import settings

class SessionExpiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if request.path != settings.LOGIN_URL:
                return redirect(settings.LOGIN_URL)
        response = self.get_response(request)
        return response
