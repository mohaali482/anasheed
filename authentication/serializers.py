from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from django.core.files.base import ContentFile
from rest_framework import serializers, validators

from .models import Image

User = get_user_model()

BASIC_USER_FIELDS = (
    "id",
    "username",
    "first_name",
    "last_name",
    "email",
    "image",
    "date_joined",
)


class AdminUserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    image = serializers.ImageField(source="image.image")
    password = serializers.CharField(
        style={"input-type": "password"},
        write_only=True,
        validators=[password_validation.validate_password],
    )
    confirm_password = serializers.CharField(
        style={"input-type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = BASIC_USER_FIELDS + (
            "is_staff",
            "is_active",
            "last_login",
            "groups",
            "user_permissions",
            "password",
            "confirm_password",
        )

    def validate(self, attrs):
        if attrs["confirm_password"] != attrs["password"]:
            raise serializers.ValidationError(
                {"confirm_password": "passwords don't match"}
            )
        return attrs

    def create(self, validated_data):
        image = validated_data.pop("image")["image"]
        password = validated_data.pop("password")
        validated_data.pop("confirm_password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        Image(user=user).image.save(image.name, ContentFile(image.read()))

        return user


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("name", "codename")
        read_only_fields = ("name", "codename")


class RegularUserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="image.image", required=False)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = BASIC_USER_FIELDS


class LoggedInUserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    image = serializers.ImageField(source="image.image")
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = BASIC_USER_FIELDS + ("permissions",)

    def update(self, instance, validated_data):
        if "image" in validated_data:
            user = self.context["request"].user
            image = validated_data.pop("image")["image"]
            image_instance, _ = Image.objects.get_or_create(user=user)
            image_instance.image = image
            image_instance.save()
        return super().update(instance, validated_data)

    def get_permissions(self, obj):
        return obj.get_all_permissions()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        style={"input-type": "password"}, write_only=True
    )
    password = serializers.CharField(
        style={"input-type": "password"},
        write_only=True,
        validators=[password_validation.validate_password],
    )
    confirm_password = serializers.CharField(
        style={"input-type": "password"}, write_only=True
    )

    def validate(self, attrs):
        if attrs["confirm_password"] != attrs["password"]:
            raise serializers.ValidationError(
                {"confirm_password": ["passwords don't match"]}
            )
        return attrs


class UserSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    image = serializers.ImageField(required=False)
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input-type": "password"},
        write_only=True,
        validators=[password_validation.validate_password],
    )
    confirm_password = serializers.CharField(
        style={"input-type": "password"}, write_only=True
    )

    def validate(self, attrs):
        if attrs["confirm_password"] != attrs["password"]:
            raise serializers.ValidationError(
                {"confirm_password": "passwords don't match"}
            )
        return attrs

    def create(self, validated_data):
        image = validated_data.pop("image")
        password = validated_data.pop("password")
        validated_data.pop("confirm_password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        user_image = Image.objects.create(user=user, image=image)
        user_image.save()

        return user

    class Meta:
        model = User
        fields = (
            "username",
            "image",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
        )


class DeleteAccountSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class PasswordResetForm(serializers.Serializer):
    email = serializers.EmailField()


class ChangePasswordForm(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    def validate_new_password(self, value):
        validate_password(value)

        return value

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError(
                {
                    "new_password": "Passwords don't match",
                }
            )

        return attrs
