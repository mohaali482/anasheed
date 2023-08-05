from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import MyNasheedModelViewSet, NasheedListAPIView

router = DefaultRouter()
router.register("my-nasheeds", MyNasheedModelViewSet, basename="my-nasheeds")
urlpatterns = [
    path("nasheeds/", NasheedListAPIView.as_view(), name="nasheeds-list"),
] + router.urls
