from rest_framework.routers import DefaultRouter

from .views import NasheedModelViewSet, SavedNasheedModelViewSet

router = DefaultRouter()
router.register("nasheeds", NasheedModelViewSet)
router.register("saved-nasheeds", SavedNasheedModelViewSet, basename="saved-nasheeds")
urlpatterns = [] + router.urls
