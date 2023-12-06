from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets

from .filters import NasheedsFilter, SavedNasheedsFilter
from .models import Nasheed, SavedNasheed
from .permissions import NasheedPermissions
from .serializers import (
    AdminUpdateNasheedSerializer,
    NasheedSerializer,
    SavedNasheedSerializer,
)


class NasheedModelViewSet(viewsets.ModelViewSet):
    serializer_class = NasheedSerializer
    queryset = Nasheed.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NasheedsFilter
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.user.is_superuser and self.action == "update":
            return AdminUpdateNasheedSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.request.user.is_staff:
            return []
        return super().get_permissions()


class MyNasheedModelViewSet(viewsets.ModelViewSet):
    serializer_class = NasheedSerializer
    queryset = Nasheed.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NasheedsFilter
    permission_classes = [permissions.IsAuthenticated, NasheedPermissions]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class SavedNasheedModelViewSet(viewsets.ModelViewSet):
    serializer_class = SavedNasheedSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SavedNasheedsFilter
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = SavedNasheed.objects.filter(user=self.request.user)
        return queryset
