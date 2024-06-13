from django.urls import path
from .views import schedule_evaluation, create_evaluation, view_evaluations, view_scheduled_evaluations, evaluation_detail, get_questions

urlpatterns = [
    path('schedule/', schedule_evaluation, name='schedule_evaluation'),
    path('create/', create_evaluation, name='create_evaluation'),
    path('view/', view_evaluations, name='view_evaluations'),
    path('scheduled/', view_scheduled_evaluations, name='view_scheduled_evaluations'),
    path('evaluation/<int:evaluation_id>/', evaluation_detail, name='evaluation_detail'),
    path('get_questions/<int:schedule_id>/', get_questions, name='get_questions'),

]
