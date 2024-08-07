from django import forms
from .models import EvaluationSchedule, Evaluation, Answer
from accounts.models import CustomUser

class EvaluationScheduleForm(forms.ModelForm):
    self_evaluation = forms.BooleanField(required=False, label='Autoavaliação')

    class Meta:
        model = EvaluationSchedule
        fields = ['evaluator', 'evaluatee', 'client', 'date_scheduled']
        labels = {
            'evaluator': 'Avaliador',
            'evaluatee': 'Avaliado',
            'client': 'Cliente',
            'date_scheduled': 'Data Agendada',
        }
        widgets = {
            'date_scheduled': forms.DateInput(attrs={'type': 'date', 'class': 'form-select'}),
            'evaluator': forms.Select(attrs={'class': 'form-select'}),
            'evaluatee': forms.Select(attrs={'class': 'form-select'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['evaluatee'].queryset = CustomUser.objects.filter(department=user.department)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-select'

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = []

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'score']
