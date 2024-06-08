# urls.py (assessments)
from django.urls import path
from .views import create_evaluation, view_evaluations

urlpatterns = [
    path('create/', create_evaluation, name='create_evaluation'),
    path('view/', view_evaluations, name='view_evaluations'),
]
