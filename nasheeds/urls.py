from rest_framework.routers import DefaultRouter

from .views import NasheedModelViewSet

router = DefaultRouter()
router.register("nasheeds", NasheedModelViewSet)
urlpatterns = [] + router.urls
