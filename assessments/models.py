from django.db import models
from django.conf import settings
from accounts.models import Client, Department, Role

class Question(models.Model):
    text = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role_type = models.IntegerField(choices=Role.ROLE_TYPE_CHOICES)
    weight_question = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return self.text

class EvaluationSchedule(models.Model):
    COMMITMENT_CHOICES = [
        ('Auditoria externa - Preliminar', 'Auditoria externa - Preliminar'),
        ('Auditoria externa - Controle Interno', 'Auditoria externa - Controle Interno'),
        ('Auditoria externa - Final', 'Auditoria externa - Final'),
        ('Inventário', 'Inventário'),
        ('Serviços Financeiros', 'Serviços Financeiros'),
        ('Auditoria Interna', 'Auditoria Interna'),
        ('Incorporação', 'Incorporação'),
        ('Auditoria Cooperativa', 'Auditoria Cooperativa'),
        ('Demonstrações Financeiras - Final', 'Demonstrações Financeiras - Final'),
        ('Demonstrações Financeiras - Preliminar', 'Demonstrações Financeiras - Preliminar'),
        ('Auditoria contínua', 'Auditoria contínua'),
        ('Revisão contábil', 'Revisão contábil'),
        ('Outros', 'Outros'),
    ]

    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluation_schedules')
    evaluatee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluation_scheduled')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=1)
    date_scheduled = models.DateField()
    self_evaluation = models.BooleanField(default=False)
    commitment = models.CharField(max_length=50, choices=COMMITMENT_CHOICES)
    other_commitment = models.CharField(max_length=255, blank=True, null=True)  # Campo para "Outros"

    def __str__(self):
        return f"Evaluation scheduled by {self.evaluator} for {self.evaluatee} on {self.date_scheduled}"


class Evaluation(models.Model):
    schedule = models.OneToOneField(EvaluationSchedule, on_delete=models.CASCADE)
    date_completed = models.DateField(auto_now_add=True)
    role_at_time = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)  


    def __str__(self):
        return f"Evaluation by {self.schedule.evaluator} for {self.schedule.evaluatee} on {self.date_completed}"

class Answer(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Answer to {self.question} with score {self.score}"
