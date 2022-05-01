from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    CommentViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserCreateAPIView,
    GetTokenAPIView,
    UserViewSet,
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(r'users', UserViewSet)
urlpatterns = [
    path('v1/auth/signup/', UserCreateAPIView.as_view()),
    path('v1/auth/token/', GetTokenAPIView.as_view()),
    path('v1/', include(router.urls)),
]
