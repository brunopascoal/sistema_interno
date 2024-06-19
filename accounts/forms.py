from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Client, CustomUser

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'responsible']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'department', 'role')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'department', 'role')
