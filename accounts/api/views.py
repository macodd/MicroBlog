from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .serializers import UserDisplaySerializer


User = get_user_model()


class UserProfileAPIView(RetrieveAPIView):
    queryset                = User.objects.all()
    lookup_field            = 'username'
    serializer_class        = UserDisplaySerializer
    permission_classes      = [IsAuthenticated]
