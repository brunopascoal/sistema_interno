# models.py (accounts)
from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

class Client(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name