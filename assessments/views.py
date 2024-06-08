# views.py (assessments)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EvaluationForm
from .models import Evaluation, Answer, Question

@login_required
def create_evaluation(request):
    if request.method == 'POST':
        evaluation_form = EvaluationForm(request.POST, evaluator=request.user)
        if evaluation_form.is_valid():
            evaluation = evaluation_form.save(commit=False)
            evaluation.evaluator = request.user
            evaluation.save()
            for question in Question.objects.all():
                score = request.POST.get(f'question_{question.id}')
                Answer.objects.create(evaluation=evaluation, question=question, score=score)
            return redirect('view_evaluations')
    else:
        evaluation_form = EvaluationForm(evaluator=request.user)
        questions = Question.objects.all()
    return render(request, 'assessments/create_evaluation.html', {
        'evaluation_form': evaluation_form,
        'questions': questions,
    })

@login_required
def view_evaluations(request):
    evaluations = Evaluation.objects.filter(evaluator=request.user)
    return render(request, 'assessments/view_evaluations.html', {
        'evaluations': evaluations,
    })
