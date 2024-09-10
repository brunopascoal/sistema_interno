# models.py (accounts)
from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Role(models.Model):
    ROLE_TYPE_CHOICES = (
        (1, 'Sênior'),
        (2, 'Assistente'),
    )

    name = models.CharField(max_length=255)
    role_type = models.IntegerField(choices=ROLE_TYPE_CHOICES)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=False)  # Novo campo para aprovação


class Client(models.Model):
    name = models.CharField(max_length=255)
    responsible = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name