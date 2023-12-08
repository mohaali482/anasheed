from rest_framework.routers import DefaultRouter

from .views import MyNasheedModelViewSet, NasheedModelViewSet, SavedNasheedModelViewSet

router = DefaultRouter()
router.register("nasheeds/", NasheedModelViewSet)
router.register("my-nasheeds/", MyNasheedModelViewSet, basename="my-nasheeds")
router.register("saved-nasheeds/", SavedNasheedModelViewSet, basename="saved-nasheeds")
urlpatterns = [] + router.urls
