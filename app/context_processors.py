from django.contrib.auth.models import Group

def control_group(request):
    # Verifica se o usuário está autenticado e se faz parte do grupo "Controle"
    is_in_control_group = request.user.is_authenticated and request.user.groups.filter(name='Controle').exists()
    return {'is_in_control_group': is_in_control_group}

def schedule_group(request):
    # Verifica se o usuário está autenticado e se faz parte do grupo "Agendamento"
    is_in_schedule_group = request.user.is_authenticated and request.user.groups.filter(name='Agendamento').exists()
    return {'is_in_schedule_group': is_in_schedule_group}

