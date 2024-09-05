import django_filters
from .models import *

class EvaluationFilter(django_filters.FilterSet):
    class Meta:
        model = Evaluation
        fields = '__all__'