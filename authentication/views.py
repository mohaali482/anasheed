from django.contrib.auth import get_user_model, update_session_auth_hash
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views, serializers
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Image
from .permissions import IsSelf
from .serializers import (
    AdminUserSerializer,
    ChangePasswordSerializer,
    DeleteAccountSerializer,
    RegularUserSerializer,
    UserSignupSerializer,
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()
    permission_classes = [
        permissions.IsAdminUser,
    ]


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RegularUserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsSelf,
    ]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        serializer = DeleteAccountSerializer(data=self.request.POST)
        if serializer.is_valid(raise_exception=True):
            user = self.get_object()
            requested_user = User.objects.filter(username=serializer.data["username"])
            if not requested_user.exists():
                raise serializers.ValidationError({"username": ["User not found"]})
            requested_user = requested_user.first()
            if user == requested_user:
                if user.check_password(serializer.data["password"]):
                    self.perform_destroy(user)
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    raise serializers.ValidationError(
                        {"password": ["Incorrect password"]}
                    )

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class UserProfileDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        return get_object_or_404(Image, user=self.request.user)


class ChangePasswordAPIView(views.APIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        data = self.serializer_class(data=request.POST)
        if data.is_valid(raise_exception=True):
            valid_password = request.user.check_password(
                data.validated_data.get("current_password")
            )
            if not valid_password:
                raise serializers.ValidationError(
                    {"current_password": ["Incorrect password"]}
                )
            user = request.user
            user.set_password(data.validated_data.get("password"))
            user.save()
            update_session_auth_hash(request, user)
            return Response(data={"msg": "success"}, status=status.HTTP_200_OK)

        return Response(data={"msg": "error"}, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if self.request.method == "DELETE":
            response.delete_cookie("refresh_token")
        elif response.data.get("refresh"):
            cookie_max_age = 3600 * 24 * 14
            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                max_age=cookie_max_age,
                httponly=True,
            )
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)

    def delete(self, request):
        return Response("success", status=status.HTTP_204_NO_CONTENT)


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh_token")
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            raise InvalidToken("No valid token found in cookie 'refresh_token'")


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                max_age=cookie_max_age,
                httponly=True,
            )
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = CookieTokenRefreshSerializer


class UserSignup(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    queryset = User.objects.all()
