from django.urls import include, path

from rest_framework import routers

from api.views import (CategoryViewSet,
                       GenreViewSet,
                       TitleViewSet,
                       get_jwt_token,
                       register,
                       UserViewSet)


V1_PATH = 'v1/'

router_v1 = routers.DefaultRouter()
router_v1.register(f'{V1_PATH}categories', CategoryViewSet)
router_v1.register(f'{V1_PATH}genres', GenreViewSet)
router_v1.register(f'{V1_PATH}titles', TitleViewSet)
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path(f'{V1_PATH}auth/signup/', register, name='register'),
    path(f'{V1_PATH}auth/token/', get_jwt_token, name='token')
]
