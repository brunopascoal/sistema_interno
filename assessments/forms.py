# forms.py (assessments)
from django import forms
from .models import Evaluation, Answer
from accounts.models import CustomUser

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['evaluatee', 'client']

    def __init__(self, *args, **kwargs):
        evaluator = kwargs.pop('evaluator', None)
        super().__init__(*args, **kwargs)
        if evaluator:
            self.fields['evaluatee'].queryset = CustomUser.objects.exclude(id=evaluator.id)

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'score']
