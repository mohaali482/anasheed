from rest_framework import serializers

from .models import Nasheed


class NasheedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nasheed
        fields = "__all__"
