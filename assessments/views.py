from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EvaluationScheduleForm, EvaluationForm
from .models import EvaluationSchedule, Evaluation, Answer, Question

@login_required
def schedule_evaluation(request):
    if request.method == 'POST':
        schedule_form = EvaluationScheduleForm(request.POST)
        if schedule_form.is_valid():
            schedule_form.save()
            return redirect('view_scheduled_evaluations')
    else:
        schedule_form = EvaluationScheduleForm()
    return render(request, 'assessments/schedule_evaluation.html', {
        'schedule_form': schedule_form,
    })

@login_required
def create_evaluation(request):
    pending_schedules = EvaluationSchedule.objects.filter(evaluator=request.user, evaluation__isnull=True)
    
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        if schedule_id:
            schedule = EvaluationSchedule.objects.get(id=schedule_id)
            evaluation = Evaluation.objects.create(schedule=schedule)
            for question in Question.objects.all():
                score = request.POST.get(f'question_{question.id}')
                Answer.objects.create(evaluation=evaluation, question=question, score=score)
            return redirect('view_evaluations')
        else:
            return render(request, 'assessments/create_evaluation.html', {
                'pending_schedules': pending_schedules,
                'questions': Question.objects.all(),
                'error': 'Selecione uma avaliação para continuar.'
            })
    
    return render(request, 'assessments/create_evaluation.html', {
        'pending_schedules': pending_schedules,
        'questions': Question.objects.all() if pending_schedules else None,
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