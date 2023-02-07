import django_filters as dj_filters

from reviews.models import Title


class TitleFilter(dj_filters.FilterSet):
    name = dj_filters.CharFilter(field_name='name', lookup_expr='contains')
    year = dj_filters.NumberFilter(field_name='year')
    category = dj_filters.CharFilter(field_name='category__slug')
    genre = dj_filters.CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = '__all__'
