from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import get_jwt_token, register, UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)

V1_PATH = 'v1/'

urlpatterns = [
    path(f'{V1_PATH}auth/signup/', register, name='register'),
    path(f'{V1_PATH}auth/token/', get_jwt_token, name='token')
]
