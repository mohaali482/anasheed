from rest_framework import serializers

from .models import Nasheed


class NasheedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nasheed
        fields = "__all__"
        read_only_fields = ["owner"]

    def create(self, validated_data):
        owner = self.context["request"].user
        validated_data["owner"] = owner
        return super().create(validated_data)


class AdminNasheedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nasheed
        fields = "__all__"
