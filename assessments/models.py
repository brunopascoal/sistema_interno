from django.db import models
from django.conf import settings
from accounts.models import Client, Department, Role

class Question(models.Model):
    text = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)  # Defina o valor padrão aqui
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=1)  # Defina o valor padrão aqui

    def __str__(self):
        return self.text

class EvaluationType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class EvaluationSchedule(models.Model):
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluation_schedules')
    evaluatee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluation_scheduled')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)  # Defina o valor padrão aqui
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=1)  # Defina o valor padrão aqui
    date_scheduled = models.DateField()
    evaluation_type = models.ForeignKey(EvaluationType, on_delete=models.CASCADE)

    def __str__(self):
        return f"Evaluation scheduled by {self.evaluator} for {self.evaluatee} on {self.date_scheduled}"

class Evaluation(models.Model):
    schedule = models.OneToOneField(EvaluationSchedule, on_delete=models.CASCADE)
    date_completed = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation by {self.schedule.evaluator} for {self.schedule.evaluatee} on {self.date_completed}"

class Answer(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"Answer to {self.question} with score {self.score}"
