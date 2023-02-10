import datetime as dt

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_username


class MetaSlug:
    '''Общий мета класс для поиска по slug.'''
    fields = ('name', 'slug',)
    lookup_field = 'slug'
    extra_kwargs = {
        'url': {'lookup_field': 'slug'}
    }


class CategorySerializer(serializers.ModelSerializer):
    '''Сериализатор для категорий.'''
    class Meta(MetaSlug):
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    '''Сериализатор для жанров.'''
    class Meta(MetaSlug):
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    '''Сериализатор для title.'''
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    def validate_year(self, year: int) -> int:
        if dt.datetime.now().year < year:
            raise serializers.ValidationError("year not valid value")
        return year

    class Meta:
        model = Title
        fields = '__all__'


class ListRetrieveTitleSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели title (list, retrieve).'''
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для юзера.'''

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class RegisterDataSerializer(serializers.Serializer):
    '''Сериализатор регистрации.'''

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    '''Сериализатор для юзера.'''
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CommentsSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели.'''
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
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
    '''Сериализатор для отзывов.'''
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    score = serializers.IntegerField(max_value=10, min_value=1)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('На произведение можно оставить'
                                      'один отзыв.')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
