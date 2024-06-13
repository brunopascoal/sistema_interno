# admin.py (assessments)
from django.contrib import admin
from .models import Question, Evaluation, Answer, EvaluationSchedule, EvaluationType

admin.site.register(Question)
admin.site.register(Evaluation)
admin.site.register(Answer)
admin.site.register(EvaluationSchedule)
admin.site.register(EvaluationType)


