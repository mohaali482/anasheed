from rest_framework import viewsets

from .models import Nasheed
from .permissions import NasheedPermissions
from .serializers import NasheedSerializer


class NasheedModelViewSet(viewsets.ModelViewSet):
    serializer_class = NasheedSerializer
    queryset = Nasheed.objects.all()
    permission_classes = [NasheedPermissions]
