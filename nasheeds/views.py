from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets

from .filters import NasheedsFilter, SavedNasheedsFilter
from .models import Nasheed, SavedNasheed
from .permissions import NasheedPermissions
from .serializers import (
    AdminNasheedSerializer,
    AdminUpdateNasheedSerializer,
    NasheedSerializer,
    SavedNasheedSerializer,
)


class NasheedModelViewSet(viewsets.ModelViewSet):
    serializer_class = NasheedSerializer
    queryset = Nasheed.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NasheedsFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, NasheedPermissions]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            if self.action == "update":
                return AdminUpdateNasheedSerializer
            return AdminNasheedSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.request.user.is_staff:
            return []
        return super().get_permissions()


class SavedNasheedModelViewSet(viewsets.ModelViewSet):
    serializer_class = SavedNasheedSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SavedNasheedsFilter
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = SavedNasheed.objects.filter(user=self.request.user)
        return queryset
