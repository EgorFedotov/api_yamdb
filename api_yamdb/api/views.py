from reviews.models import Category, Genre
from .serializers import CategorySerializer, GenreSerializer
from .mixins import ListCreateDestroyViewSet


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
