from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ChangePasswordAPIView,
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    UserRetrieveUpdateAPIView,
    UserSignup,
    UserViewSet,
)

router = DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("token", CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path(
        "me", UserRetrieveUpdateAPIView.as_view(), name="user_retrieve_update_api_view"
    ),
    path("me/change-password", ChangePasswordAPIView.as_view(), name="change-password"),
    path("signup", UserSignup.as_view(), name="user_signup"),
] + router.urls
