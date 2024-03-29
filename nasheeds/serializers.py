from authentication.serializers import RegularUserSerializer
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import serializers

from .models import Nasheed, SavedNasheed

User = get_user_model()


class NasheedSerializer(serializers.ModelSerializer):
    owner = RegularUserSerializer(read_only=True)
    duration = serializers.ReadOnlyField()

    def to_representation(self, instance):
        request = self.context.get("request", None)
        fields = super().to_representation(instance)
        if request is None:
            return fields

        user = request.user
        if user is None or not user.is_authenticated:
            return fields

        saved = instance.savednasheed_set.filter(user=user)
        fields["saved"] = saved.exists()

        if saved.exists():
            fields["saved_id"] = saved.first().id

        return fields

    class Meta:
        model = Nasheed
        fields = "__all__"
        read_only_fields = ["owner"]

    def create(self, validated_data):
        owner = self.context["request"].user
        validated_data["owner"] = owner
        return super().create(validated_data)


class AdminUpdateNasheedSerializer(serializers.ModelSerializer):
    duration = serializers.ReadOnlyField()

    class Meta:
        model = Nasheed
        fields = "__all__"


class SavedNasheedSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        fields = NasheedSerializer().to_representation(instance=instance.nasheed)
        fields["saved"] = True
        fields["saved_id"] = instance.id
        return fields

    class Meta:
        model = SavedNasheed
        fields = ("nasheed",)

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request is None:
            raise serializers.ValidationError({"user": "user cannot be null"})

        user = request.user
        if user is None:
            raise serializers.ValidationError({"user": "user cannot be null"})

        validated_data["user"] = user
        try:
            instance = super().create(validated_data)
        except IntegrityError as err:
            if (
                str(err)
                == "UNIQUE constraint failed: nasheeds_savednasheed.user_id, nasheeds_savednasheed.nasheed_id"
            ):
                raise serializers.ValidationError(
                    {"nasheed": "you've already saved this nasheed"}
                )

        return instance
