# models.py (assessments)
from django.db import models
from django.conf import settings
from accounts.models import Client

class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Evaluation(models.Model):
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluations_given')
    evaluatee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluations_received')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation by {self.evaluator} for {self.evaluatee} on {self.date}"

class Answer(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"Answer to {self.question} with score {self.score}"
