from django.urls import path
from .views import schedule_evaluation, create_evaluation, view_evaluations, view_scheduled_evaluations, evaluation_detail, get_questions, export_evaluation, export_all_evaluations, analysis, delete_selected_schedules, edit_evaluation_schedule
urlpatterns = [
    path('schedule/', schedule_evaluation, name='schedule_evaluation'),
    path('create/', create_evaluation, name='create_evaluation'),
    path('view/', view_evaluations, name='view_evaluations'),
    path('scheduled/', view_scheduled_evaluations, name='view_scheduled_evaluations'),
    path('edit-schedule/<int:schedule_id>/', edit_evaluation_schedule, name='edit_evaluation_schedule'),
    path('schedule/delete_selected/', delete_selected_schedules, name='delete_selected_schedules'),
    path('evaluation/<int:evaluation_id>/', evaluation_detail, name='evaluation_detail'),
    path('get_questions/<int:schedule_id>/', get_questions, name='get_questions'),
    path('export/evaluation/<int:evaluation_id>/', export_evaluation, name='export_evaluation'),
    path('export/all/', export_all_evaluations, name='export_all_evaluations'),
    path('analysis/', analysis, name='analysis'),



]
