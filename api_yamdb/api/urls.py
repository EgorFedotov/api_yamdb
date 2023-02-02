
from django.urls import include, path

from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet


V1_PATH = 'v1/'

router_v1 = routers.DefaultRouter()
router_v1.register(f'{V1_PATH}categories', CategoryViewSet)
router_v1.register(f'{V1_PATH}genres', GenreViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
]
