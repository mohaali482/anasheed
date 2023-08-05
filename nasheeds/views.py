from rest_framework import generics, permissions, viewsets

from .models import Nasheed
from .permissions import NasheedPermissions
from .serializers import (
    AdminNasheedSerializer,
    AdminUpdateNasheedSerializer,
    NasheedSerializer,
)


class NasheedListAPIView(generics.ListAPIView):
    serializer_class = NasheedSerializer
    queryset = Nasheed.objects.all()


class MyNasheedModelViewSet(viewsets.ModelViewSet):
    serializer_class = NasheedSerializer
    permission_classes = [permissions.IsAuthenticated, NasheedPermissions]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            if self.action == "update":
                return AdminUpdateNasheedSerializer
            return AdminNasheedSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = Nasheed.objects.filter(owner=self.request.user)
        return queryset

    def get_permissions(self):
        if self.request.user.is_staff:
            return []
        return super().get_permissions()
