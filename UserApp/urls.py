from django.urls import path,include
from .views import UserCreateView, UserViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('', include(router.urls)),
]

