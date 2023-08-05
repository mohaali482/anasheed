from rest_framework import permissions, viewsets

from .models import Nasheed
from .permissions import NasheedPermissions
from .serializers import (
    AdminNasheedSerializer,
    AdminUpdateNasheedSerializer,
    NasheedSerializer,
)


class NasheedModelViewSet(viewsets.ModelViewSet):
    serializer_class = NasheedSerializer
    queryset = Nasheed.objects.all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, NasheedPermissions]

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
