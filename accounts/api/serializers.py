from django.contrib.auth.models import User
from rest_framework import serializers
from django.urls import reverse_lazy

from accounts.models import UserProfile


class UsernameTakenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username'
        ]
        read_only_fields = [
            'username'
        ]


class UserDisplaySerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField(source='get_follower_count')
    url = serializers.SerializerMethodField(source='get_url')
    image = serializers.SerializerMethodField(source='get_image')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'follower_count',
            'image',
            'url',
        ]

    def get_image(self, obj):
        qs = UserProfile.objects.filter(user__username=obj)
        return qs.first().image.url

    def get_follower_count(self, obj):
        qs = UserProfile.objects.filter(user__username=obj)
        profile = qs.first()
        return profile.get_following().count()

    def get_url(self, obj):
        return reverse_lazy('profiles:detail', kwargs={'username': obj.username})
