from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def register_view(request):
    user_form = UserCreationForm()
    if request.method == "POST":

        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect("login")
    return render(request, "register.html", {"user_form": user_form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            login_form = AuthenticationForm()
    else:
        login_form = AuthenticationForm()

    return render(request, "login.html", {'login_form': login_form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def homepage_view(request):
    return render(request, "homepage.html")