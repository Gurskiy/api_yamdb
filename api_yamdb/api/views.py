from django.shortcuts import render
from rest_framework import filters, viewsets
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Review, Comment
from .mixins import BaseCreateListDestroyViewSet
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentsSerializer,
    GenreSerializer,
    ReviewSerializer,
)


class CategoryViewSet(BaseCreateListDestroyViewSet):
    """Вьюсет для категорий"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(BaseCreateListDestroyViewSet):
    """Вьюсет для жанра"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев"""

    # queryset = Comment.objects.all()
    serializer_class = CommentsSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        # serializer.save(author=self.request.user, review=review)
        serializer.save(review=review)
