from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, CommentViewSet, ReviewViewSet


router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"genres", GenreViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register(r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet)
urlpatterns = [
    path("v1/", include(router.urls)),
]
