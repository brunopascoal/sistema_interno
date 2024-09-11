from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.views import homepage_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage_view, name='homepage'),  # Página inicial do site
    path('accounts/', include('accounts.urls')),  # Inclui as URLs do aplicativo accounts
    path('assessments/', include('assessments.urls')),  # Inclui as URLs do aplicativo assessments

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
