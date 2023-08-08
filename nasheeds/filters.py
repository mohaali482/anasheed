from django_filters import rest_framework as filters

from .models import Nasheed, SavedNasheed


class NasheedsFilter(filters.FilterSet):
    class Meta:
        model = Nasheed
        fields = {"owner": ("exact",), "name": ("contains",)}


class SavedNasheedsFilter(filters.FilterSet):
    class Meta:
        model = SavedNasheed
        fields = {"nasheed__name": ("contains",)}
