import random
import string

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, User

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категорий"""

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанр"""

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""

    def create(self, validated_data):
        confirmation_code = ''.join(
            (random.choice(string.ascii_letters) for i in range(16))
        )
        send_mail(
            'Код подтверждения от сервиса yamdb',
            f'Ваш код подтверждения - {confirmation_code}',
            'admin@yamdb.com',
            [validated_data['email']]
        )
        return User.objects.create(
            confirmation_code=confirmation_code,
            role='user',
            **validated_data
        )

    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена"""
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=16)
    token = serializers.SerializerMethodField()

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])

        if data['confirmation_code'] != user.confirmation_code:
            raise serializers.ValidationError('неверный код подтверждения')

        return data

    def get_token(self, obj):
        user = User.objects.get(username=obj['username'])
        token = get_tokens_for_user(user)['access']
        return token


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя"""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
