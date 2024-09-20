from django import forms
from .models import EvaluationSchedule, Evaluation, Answer
from accounts.models import CustomUser, Client


# forms.py

class EvaluationScheduleForm(forms.Form):
    evaluator = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Avaliador',
        empty_label=None  # Remove a opção vazia

    )
    evaluatee = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        label='Avaliado'
    )
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Cliente'
    )
    date_scheduled = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-select'}),
        label='Data Agendada'
    )

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

class AnalysisForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), label="Usuário", widget=forms.Select(attrs={'class': 'form-select'}))
    start_date = forms.DateField(label="Data Inicial", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-select'}))
    end_date = forms.DateField(label="Data Final", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-select'}))