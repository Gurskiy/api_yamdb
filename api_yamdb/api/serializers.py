import random
import string

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, Comment, Review, User


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
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанр"""

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели title (create, change, destroy)"""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ListRetrieveTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели title (list, retrieve)"""
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментария"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатов для отзывов"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    score = serializers.IntegerField(max_value=10, min_value=1)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Нельзя добавить более одного отзыва'
                                      'на произведение')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не может быть использовано'
            )
        return value

    def create(self, validated_data):
        confirmation_code = ''.join(
            (random.choice(string.ascii_letters) for i in range(16))
        )
        send_mail(
            'Код подтверждения от сервиса yamdb',
            f'Ваш код подтверждения - {confirmation_code}',
            'admin@yamdb.com',
            [validated_data['email']],
        )
        return User.objects.create(
            confirmation_code=confirmation_code, role='user', **validated_data
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
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения своей учетной записи"""
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
