from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import get_user_model

from .serializers import UserDisplaySerializer

from accounts.models import UserProfile


class UserProfileAPIView(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    lookup_field = 'user'
    serializer_class = UserDisplaySerializer
    permission_classes = [IsAuthenticated]
