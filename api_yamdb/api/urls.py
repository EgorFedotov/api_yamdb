
from django.urls import include, path

from rest_framework import routers

from api.views import CategoryViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r'categories', CategoryViewSet)


V1_PATH = 'v1/'

urlpatterns = [
    path('', include(router_v1.urls)),
]
