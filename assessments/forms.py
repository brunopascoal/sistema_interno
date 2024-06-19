from django import forms
from .models import EvaluationSchedule, Evaluation, Answer
from accounts.models import CustomUser

class EvaluationScheduleForm(forms.ModelForm):
    class Meta:
        model = EvaluationSchedule
        fields = ['evaluatee', 'client', 'date_scheduled', 'evaluation_type']
        widgets = {
            'date_scheduled': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['evaluatee'].queryset = CustomUser.objects.filter(department=user.department)

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = []

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'score']
