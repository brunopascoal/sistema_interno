from django import forms
from .models import EvaluationSchedule, Evaluation, Answer
from accounts.models import CustomUser

class EvaluationScheduleForm(forms.ModelForm):
    class Meta:
        model = EvaluationSchedule
        fields = ['evaluator', 'evaluatee', 'client', 'date_scheduled']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['evaluator'].queryset = CustomUser.objects.filter(role__name='Avaliador')
        self.fields['evaluatee'].queryset = CustomUser.objects.filter(role__name='Avaliado')

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = []

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'score']
