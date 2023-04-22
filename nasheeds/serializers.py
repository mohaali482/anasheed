from authentication.serializers import RegularUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Nasheed

User = get_user_model()


class NasheedSerializer(serializers.ModelSerializer):
    owner = RegularUserSerializer(read_only=True)

    class Meta:
        model = Nasheed
        fields = "__all__"
        # read_only_fields = ["owner"]

    def create(self, validated_data):
        # owner = self.context["request"].user
        from django.contrib.auth import get_user_model

        user = get_user_model()
        owner = user.objects.all().first()
        validated_data["owner"] = owner
        return super().create(validated_data)


class AdminNasheedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nasheed
        fields = "__all__"

    def to_representation(self, instance):
        self.fields["owner"] = RegularUserSerializer(read_only=True)
        return super().to_representation(instance)


class AdminUpdateNasheedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nasheed
        fields = "__all__"
