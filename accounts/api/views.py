from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth.models import User

from .serializers import UserDisplaySerializer, UsernameTakenSerializer


class UserProfileAPIView(RetrieveAPIView):
    queryset                = User.objects.all()
    lookup_field            = 'username'
    serializer_class        = UserDisplaySerializer
    permission_classes      = [IsAuthenticated]


class UsernameTakenAPIView(RetrieveAPIView):
    queryset                = User.objects.all()
    lookup_field            = 'username'
    serializer_class        = UsernameTakenSerializer
    permission_classes      = [AllowAny]
