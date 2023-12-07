from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ChangePasswordAPIView,
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    ForgotPasswordAPIView,
    PasswordResetAPIView,
    UserRetrieveUpdateDestroyAPIView,
    UserProfileDestroyAPIView,
    UserSignup,
    UserViewSet,
)

router = DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("token", CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path(
        "me",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user_retrieve_update_api_view",
    ),
    path(
        "me/delete-image",
        UserProfileDestroyAPIView.as_view(),
        name="user_profile_destroy_api_view",
    ),
    path("me/change-password", ChangePasswordAPIView.as_view(), name="change-password"),
    path("signup", UserSignup.as_view(), name="user_signup"),
    path("forgot-password", ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path(
        "reset-password/<slug:uid>/<slug:token>",
        PasswordResetAPIView.as_view(),
        name="reset-password",
    ),
] + router.urls
