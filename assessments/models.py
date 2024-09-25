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
    
class Work(models.Model):
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
    name = models.CharField("Nome do Trabalho", max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")
    date_scheduled = models.DateField("Data Agendada")
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='works_responsible',
        verbose_name="Responsável"
    )
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='works_evaluator',
        verbose_name="Avaliador"
    )
    evaluatees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='works_evaluatees',
        verbose_name="Avaliados"
    )
    commitment = models.CharField(
        "Compromisso",
        max_length=50,
        choices=COMMITMENT_CHOICES,
        blank=True,
        null=True
    )
    other_commitment = models.CharField(
        "Outro Compromisso",
        max_length=255,
        blank=True,
        null=True
    )
    def __str__(self):
        return f"{self.name} - {self.client.name}"

# models.py (assessments)

class EvaluationSchedule(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, verbose_name="Trabalho", null=True, blank=True)
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='evaluation_schedules',
        verbose_name="Avaliador"
    )
    evaluatee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='evaluation_scheduled',
        verbose_name="Avaliado"
    )
    self_evaluation = models.BooleanField("Autoavaliação", default=False)

    def __str__(self):
        return f"{self.evaluator.get_full_name()} avalia {self.evaluatee.get_full_name()} no trabalho {self.work.name}"



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
