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
        fields = ['username', 'first_name', 'last_name', 'email', 'department', 'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@moorebrasil.com.br'):
            raise forms.ValidationError("Você só pode se registrar com um email @moorebrasil.com.br")
        return email

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'department', 'role', 'is_approved')
