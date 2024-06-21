from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EvaluationScheduleForm, EvaluationForm
from .models import EvaluationSchedule, Evaluation, Answer, Question
from django.http import JsonResponse

@login_required
def schedule_evaluation(request):
    if request.method == 'POST':
        form = EvaluationScheduleForm(request.POST, user=request.user)
        if form.is_valid():
            schedule = form.save(commit=False)
            #schedule.evaluator = request.user  # Define o avaliador como o usuário logado
            schedule.department = request.user.department  # Define o departamento automaticamente
            schedule.role = request.user.role  # Define o cargo automaticamente
            schedule.save()
            return redirect('view_scheduled_evaluations')
    else:
        form = EvaluationScheduleForm(user=request.user)
    return render(request, 'assessments/schedule_evaluation.html', {'form': form})

@login_required
def create_evaluation(request):
    pending_schedules = EvaluationSchedule.objects.filter(evaluator=request.user, evaluation__isnull=True)
    
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        if schedule_id:
            schedule = get_object_or_404(EvaluationSchedule, id=schedule_id)
            evaluation = Evaluation.objects.create(schedule=schedule)
            role_type = schedule.evaluatee.role.role_type
            questions = Question.objects.filter(department=schedule.department, role_type=role_type)
            for question in questions:
                score = request.POST.get(f'question_{question.id}')
                comment = request.POST.get(f'comment_{question.id}')
                Answer.objects.create(evaluation=evaluation, question=question, score=score, comment=comment)
            return redirect('view_evaluations')
    
    return render(request, 'assessments/create_evaluation.html', {
        'pending_schedules': pending_schedules,
    })

@login_required
def view_evaluations(request):
    evaluations = Evaluation.objects.filter(schedule__evaluator=request.user)
    return render(request, 'assessments/view_evaluations.html', {
        'evaluations': evaluations,
    })

@login_required
def view_scheduled_evaluations(request):
    scheduled_evaluations = EvaluationSchedule.objects.filter(evaluation__isnull=True)
    return render(request, 'assessments/view_scheduled_evaluations.html', {
        'scheduled_evaluations': scheduled_evaluations,
    })


@login_required
def evaluation_detail(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    answers = Answer.objects.filter(evaluation=evaluation)
    return render(request, 'assessments/evaluation_detail.html', {
        'evaluation': evaluation,
        'answers': answers,
    })

@login_required
def get_questions(request, schedule_id):
    schedule = get_object_or_404(EvaluationSchedule, id=schedule_id)
    role_type = schedule.evaluatee.role.role_type
    questions = Question.objects.filter(department=schedule.department, role_type=role_type)
    questions_data = [{'id': question.id, 'text': question.text} for question in questions]
    return JsonResponse({'questions': questions_data})