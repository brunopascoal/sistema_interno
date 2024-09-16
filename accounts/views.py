from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ClientForm, CustomUserCreationForm, CustomUserChangeForm
from .models import Client, CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Função para verificar se o usuário está no grupo 'controle'
def is_in_control_group(user):
    return user.is_authenticated and user.groups.filter(name='Controle').exists()

# views.py
# views.py
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False  # O usuário não será aprovado automaticamente
            user.save()
            messages.success(request, 'Conta criada com sucesso.')
            return redirect('login')  # Redireciona para a página de login após o registro
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


@user_passes_test(is_in_control_group)
@login_required
def list_users(request):
    users = CustomUser.objects.all()
    return render(request, 'users/list_users.html', {'users': users})

@user_passes_test(is_in_control_group)
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

@user_passes_test(is_in_control_group)
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

@user_passes_test(is_in_control_group)
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('list_users')
    return render(request, 'users/delete_user.html', {'user': user})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_approved:  # Verifica se o usuário está ativo
                login(request, user)
                return redirect('homepage')
            else:
                error_message = "Sua conta está desativada. Entre em contato com o administrador."
        else:
            error_message = "Usuário ou senha incorretos."
    else:
        error_message = None

    return render(request, "login.html", {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

@user_passes_test(is_in_control_group)
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

@user_passes_test(is_in_control_group)
@login_required
def list_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients/list_clients.html', {'clients': clients})

@user_passes_test(is_in_control_group)
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

@user_passes_test(is_in_control_group)
@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('list_clients')
    return render(request, 'clients/delete_client.html', {'client': client})


@csrf_exempt
def keep_session_alive(request):
    return JsonResponse({'status': 'success'})