from typing import OrderedDict
import django_filters

from .models import *

class CollegeFilter(django_filters.FilterSet):
    college_id = django_filters.CharFilter()
    college_name = django_filters.CharFilter(lookup_expr='iexact')
    university__uni_name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        models = College
        # fields = [
        #     'college_id',
        #     'college_name',
        #     'university__uni_name'
        # ]
