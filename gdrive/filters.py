from .models import *
import django_filters
from django_filters import DateFilter, CharFilter

class UserFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = UserFiles
        exclude = ['customer', 'date_created', 'file_name']
