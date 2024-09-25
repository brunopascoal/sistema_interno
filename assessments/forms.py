from django import forms
from .models import EvaluationSchedule, Evaluation, Answer, Work
from accounts.models import CustomUser, Client


class ScheduleForm(forms.ModelForm):
    COMMITMENT_CHOICES = [
        ('Auditoria externa - Preliminar', 'Auditoria externa - Preliminar'),
        ('Auditoria externa - Controle Interno', 'Auditoria externa - Controle Interno'),
        ('Auditoria externa - Final', 'Auditoria externa - Final'),
        ('Inventário', 'Inventário'),
        ('Serviços Financeiros', 'Serviços Financeiros'),
        ('Auditoria Interna', 'Auditoria Interna'),
        ('Incorporação', 'Incorporação'),
        ('Auditoria Cooperativa', 'Auditoria Cooperativa'),
        ('Demonstrações Financeiras - Final', 'Demonstrações Financeiras - Final'),
        ('Demonstrações Financeiras - Preliminar', 'Demonstrações Financeiras - Preliminar'),
        ('Auditoria contínua', 'Auditoria contínua'),
        ('Revisão contábil', 'Revisão contábil'),
        ('Outros', 'Outros'),
    ]

    class Meta:
        model = Work
        fields = ['name', 'client', 'date_scheduled', 'responsible', 'evaluator', 'commitment', 'other_commitment', 'evaluatees']

    # Para widgets personalizados
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Cliente'
    )
    date_scheduled = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-select'}),
        label='Data Agendada'
    )
    responsible = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Responsável'
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ScheduleForm, self).__init__(*args, **kwargs)
    
        if user:
            # Filtrar avaliadores e avaliados pelo departamento do usuário logado e excluir usuários sem departamento
            department = user.department
            if department:
                self.fields['evaluator'].queryset = CustomUser.objects.filter(is_active=True, department=department).exclude(department__isnull=True)
                self.fields['evaluatees'].queryset = CustomUser.objects.filter(is_active=True, department=department).exclude(department__isnull=True)
            else:
                # Caso o usuário logado não tenha um departamento, você pode lidar com isso conforme a sua necessidade
                self.fields['evaluator'].queryset = CustomUser.objects.none()
                self.fields['evaluatees'].queryset = CustomUser.objects.none()

    evaluator = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Avaliador'
    )
    
    evaluatees = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(is_active=True),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        label='Avaliados'
    )

    commitment = forms.ChoiceField(
        choices=COMMITMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Compromisso'
    )
    other_commitment = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Outro Compromisso'
    )

    def clean(self):
        cleaned_data = super().clean()
        commitment = cleaned_data.get('commitment')
        other_commitment = cleaned_data.get('other_commitment')

        if commitment == 'Outros' and not other_commitment:
            self.add_error('other_commitment', 'Por favor, especifique o compromisso.')


        
class EvaluationScheduleForm(forms.Form):
    evaluator = forms.ModelChoiceField(
        queryset=CustomUser.objects.none(),
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

        # Filtra os avaliadores e avaliados pelo departamento do usuário logado
        self.fields['evaluator'].queryset = CustomUser.objects.filter(department=user.department)
        self.fields['evaluatee'].queryset = CustomUser.objects.filter(department=user.department)

        # Adiciona a classe 'form-select' aos campos
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