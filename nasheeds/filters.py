from django_filters import rest_framework as filters

from .models import Nasheed


class NasheedsFilter(filters.FilterSet):
    class Meta:
        model = Nasheed
        fields = {"owner": ("exact",), "name": ("contains",)}
