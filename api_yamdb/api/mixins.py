from rest_framework import mixins, permissions, filters
from rest_framework.viewsets import GenericViewSet


class ListCreateDestroyViewSet(mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               GenericViewSet):
    pass


class AdminControlSlugViewSet(ListCreateDestroyViewSet):
    '''Общий родительский класс для категорий и жанров.'''
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]
    lookup_field = 'slug'
    permission_classes = (permissions.IsAdminUser,)
