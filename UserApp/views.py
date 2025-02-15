from rest_framework import generics,status
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .constants import *
import logging
from django.http import HttpResponse

logger = logging.getLogger("django")


def HomePage(request):
    return HttpResponse("Welcome!")

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)  # Includes `id`
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e))
            return Response({"error": GLOBAL_ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """Allow admins to create/update/delete, regular users can only retrieve."""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def update(self, request, *args, **kwargs):
        try:
            """ Ensure updated data is returned after saving """
            instance = self.get_object()  # Get current user object
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            instance.refresh_from_db()  # Ensure fresh data is loaded
            return Response(UserSerializer(instance).data)
        except Exception as e:
            logger.error(str(e))
            return Response({"error": GLOBAL_ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)