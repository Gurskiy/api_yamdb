from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from reviews.models import Category, Genre, User
from .mixins import BaseCreateListDestroyViewSet
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, \
    UserCreateSerializer, GetTokenSerializer, UserSerializer


class CategoryViewSet(BaseCreateListDestroyViewSet):
    """Вьюсет для категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(BaseCreateListDestroyViewSet):
    """Вьюсет для жанра"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class UserCreateAPIView(APIView):
    """Регистрация нового пользователя"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'user': serializer.data})


class GetTokenAPIView(APIView):
    """Получение токена пользователем"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"token": serializer.data['token']})


class MyProfileAPIView(generics.RetrieveUpdateAPIView):
    """Получение/изменения данных своей учетной записи"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = User.objects.get(username=self.request.user)
        return obj


class UserViewSet(viewsets.ModelViewSet):
    """Получение списка пользователей/добавления пользователся админом"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'username'
