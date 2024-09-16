from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Client, CustomUser

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'responsible']


# forms.py

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'department', 'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@moorebrasil.com.br'):
            raise forms.ValidationError("Você só pode se registrar com um email @moorebrasil.com.br")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isalnum():
            raise forms.ValidationError("O nome de usuário deve conter apenas letras e números.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Verificar se as senhas correspondem
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não correspondem.")

        # Validação personalizada para a senha (por exemplo, mínimo de 8 caracteres)
        if password1 and len(password1) < 8:
            raise forms.ValidationError("A senha deve ter pelo menos 8 caracteres.")
        
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError('O primeiro nome deve conter apenas letras.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError('O último nome deve conter apenas letras.')
        return last_name



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'department', 'role', 'is_approved')
