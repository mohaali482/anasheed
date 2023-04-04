from rest_framework import permissions, viewsets

from .models import Nasheed
from .permissions import NasheedPermissions
from .serializers import NasheedSerializer


class NasheedModelViewSet(viewsets.ModelViewSet):
    serializer_class = NasheedSerializer
    queryset = Nasheed.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, NasheedPermissions]
