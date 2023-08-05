from django.contrib.auth import get_user_model, update_session_auth_hash
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .permissions import IsSelf
from .serializers import (
    AdminUserSerializer,
    ChangePasswordSerializer,
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


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = RegularUserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsSelf,
    ]

    def get_object(self):
        return self.request.user


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh_token")
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            raise InvalidToken("No valid token found in cookie 'refresh_token'")


class ChangePasswordAPIView(views.APIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        data = self.serializer_class(data=request.POST)
        if data.is_valid(raise_exception=True):
            user = request.user
            user.set_password(data.validated_data.get("password"))
            user.save()
            update_session_auth_hash(request, user)
            return Response(data={"msg": "success"}, status=status.HTTP_200_OK)

        return Response(data={"msg": "error"}, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenObtainPairView(TokenObtainPairView):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if user.is_admin:
            token["admin"] = True

        return token

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
