from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Title, User, Review

from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          RegisterDataSerializer,
                          TokenSerializer,
                          UserSerializer,
                          CommentsSerializer,
                          ReviewSerializer,
                          UserEditSerializer)


from .mixins import AdminControlSlugViewSet, ListCreateDestroyViewSet

from .permissions import AdminOnly, AdminOrReadOnly, IsAuthorOrModerOrAdmin


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    '''Регистрация пользователя.'''
    if User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    ).exists():
        return Response(request.data, status=status.HTTP_200_OK)
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, create = User.objects.get_or_create(
            **serializer.validated_data
        )
    except IntegrityError:
        raise ValidationError('Неверное имя пользователя или email')
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="YaMDb registration",
        message=f"Your confirmation code: {confirmation_code}",
        from_email=None,
        recipient_list=[user.email],
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    '''Получение токена.'''
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )

    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    '''Вьюсет для юзера.'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    @action(
        methods=[
            'get',
            'patch',
        ],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewSet(ListCreateDestroyViewSet):
    '''Набор для категорий.'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # TODO: AdminControlSlugViewSet
    filter_backends = [filters.SearchFilter]
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    search_fields = ['=name', ]
    lookup_field = 'slug'


class GenreViewSet(AdminControlSlugViewSet):
    '''Набор для жанров.'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    serializer_class = TitleSerializer
    queryset = (
        Title.objects.all()
    )
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination


class CommentViewSet(ModelViewSet):
    """Вьюсет для комментариев"""
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrModerOrAdmin,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(ModelViewSet):
    """Вьюсет для отзывов"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModerOrAdmin,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
