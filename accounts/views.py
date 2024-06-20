from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ClientForm, CustomUserCreationForm, CustomUserChangeForm
from .models import Client, CustomUser

@login_required
def list_users(request):
    users = CustomUser.objects.all()
    return render(request, 'users/list_users.html', {'users': users})

@login_required
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_users')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/add_user.html', {'form': form})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('list_users')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form, 'user': user})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('list_users')
    return render(request, 'users/delete_user.html', {'user': user})

# def register_view(request):
#     user_form = UserCreationForm()
#     if request.method == "POST":

#         user_form = UserCreationForm(request.POST)
#         if user_form.is_valid():
#             user_form.save()
#             return redirect("login")
#     return render(request, "register.html", {"user_form": user_form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            login_form = AuthenticationForm(request, data=request.POST)
            error_message = "Usuário ou senha incorretos."
    else:
        login_form = AuthenticationForm()
        error_message = None

    return render(request, "login.html", {'login_form': login_form, 'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def homepage_view(request):
    return render(request, "homepage.html")

@login_required
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_clients')
    else:
        form = ClientForm()
    return render(request, 'clients/add_client.html', {'form': form})

@login_required
def list_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients/list_clients.html', {'clients': clients})

@login_required
def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('list_clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/edit_client.html', {'form': form, 'client': client})

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('list_clients')
    return render(request, 'clients/delete_client.html', {'client': client})