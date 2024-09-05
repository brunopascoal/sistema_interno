from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EvaluationScheduleForm
from .models import EvaluationSchedule, Evaluation, Answer, Question
from accounts.models import CustomUser
from django.http import JsonResponse
import pandas as pd
from django.http import HttpResponse, JsonResponse
import matplotlib.pyplot as plt
from django import forms
import altair as alt
from django.utils.safestring import mark_safe
from django.db import models  # Adicione esta linha no início da views.py
import json
from django.db.models import Avg




@login_required
def schedule_evaluation(request):
    if request.method == 'POST':
        form = EvaluationScheduleForm(request.POST, user=request.user)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.department = request.user.department  # Define o departamento automaticamente
            schedule.role = request.user.role  # Define o cargo automaticamente
            
            # Verifica se é uma autoavaliação
            if schedule.evaluator == schedule.evaluatee:
                schedule.self_evaluation = True  # Marca como autoavaliação automaticamente
            
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

            # Criação da avaliação (autoavaliação ou regular)
            evaluation = Evaluation.objects.create(schedule=schedule, role_at_time=schedule.evaluatee.role)
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

@login_required
def export_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    answers = Answer.objects.filter(evaluation=evaluation)
    
    data = {
        'Pergunta': [answer.question.text for answer in answers],
        'Nota': [answer.score for answer in answers],
        'Comentário': [answer.comment for answer in answers],
    }

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="avaliacao_{evaluation_id}.xlsx"'
    df.to_excel(response, index=False)

    return response

@login_required
def export_all_evaluations(request):
    evaluations = Evaluation.objects.all()
    data = []

    for evaluation in evaluations:
        answers = Answer.objects.filter(evaluation=evaluation)
        for answer in answers:
            data.append({
                'Avaliador': evaluation.schedule.evaluator.username,
                'Avaliado': evaluation.schedule.evaluatee.username,
                'Cliente': evaluation.schedule.client.name,
                'Departamento': evaluation.schedule.department.name,
                'Cargo': evaluation.schedule.role.name,
                'Data Agendada': evaluation.schedule.date_scheduled,
                'Data Concluída': evaluation.date_completed,
                'Pergunta': answer.question.text,
                'Nota': answer.score,
                'Comentário': answer.comment,
            })

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="avaliacoes.xlsx"'
    df.to_excel(response, index=False)

    return response


@login_required
def export_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    data = []

    answers = Answer.objects.filter(evaluation=evaluation)
    for answer in answers:
        data.append({
            'Avaliador': evaluation.schedule.evaluator.username,
            'Avaliado': evaluation.schedule.evaluatee.username,
            'Cliente': evaluation.schedule.client.name,
            'Departamento': evaluation.schedule.department.name,
            'Cargo': evaluation.schedule.role.name,
            'Data Agendada': evaluation.schedule.date_scheduled,
            'Data Concluída': evaluation.date_completed,
            'Pergunta': answer.question.text,
            'Nota': answer.score,
            'Comentário': answer.comment,
        })

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Avaliação de {evaluation.schedule.evaluatee.username}.xlsx"'
    df.to_excel(response, index=False)

    return response



class AnalysisForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), label="Usuário", widget=forms.Select(attrs={'class': 'form-select'}))
    start_date = forms.DateField(label="Data Inicial", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-select'}))
    end_date = forms.DateField(label="Data Final", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-select'}))

@login_required
def analysis(request):
    form = AnalysisForm()

    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Filtra as avaliações normais e autoavaliações
            normal_evaluations = Evaluation.objects.filter(
                schedule__evaluatee=user,
                date_completed__range=[start_date, end_date],
                schedule__self_evaluation=False
            )
            self_evaluations = Evaluation.objects.filter(
                schedule__evaluatee=user,
                date_completed__range=[start_date, end_date],
                schedule__self_evaluation=True
            )

            questions = Question.objects.filter(department=user.department, role_type=user.role.role_type)
            
            data = []
            
            for question in questions:
                normal_scores = Answer.objects.filter(evaluation__in=normal_evaluations, question=question).values_list('score', flat=True)
                self_scores = Answer.objects.filter(evaluation__in=self_evaluations, question=question).values_list('score', flat=True)

                if normal_scores:
                    avg_normal = sum(normal_scores) / len(normal_scores)
                    data.append({'Pergunta': question.text, 'Tipo': 'Avaliação', 'Média': avg_normal})

                if self_scores:
                    avg_self = sum(self_scores) / len(self_scores)
                    data.append({'Pergunta': question.text, 'Tipo': 'Autoavaliação', 'Média': avg_self})

            df = pd.DataFrame(data)
            
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Pergunta:N', title=None, axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('Média:Q', title=None),
                color='Tipo:N',
                xOffset='Tipo:N',  # Isso permite o deslocamento das barras para o mesmo eixo x
                tooltip=['Pergunta:N', 'Tipo:N', 'Média:Q']
            ).properties(
                width=600,
                height=400,
                title=f'Média das Notas por Pergunta para {user.username}'
            ).interactive()



            chart_json = chart.to_json()

            return render(request, 'assessments/analysis.html', {'form': form, 'chart': mark_safe(chart_json)})

    return render(request, 'assessments/analysis.html', {'form': form})
