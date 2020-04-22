from rest_framework import serializers
from django.utils.timesince import timesince

from tweets.models import Tweet
from accounts.api.serializers import UserDisplaySerializer


class ParentTweetModelSerializer(serializers.ModelSerializer):
    user            = UserDisplaySerializer(read_only=True)
    date_display    = serializers.SerializerMethodField(source='get_date_display')

    class Meta:
        model = Tweet
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
        ]

    def get_date_display(self, obj):
        if obj.timestamp.hour < 5:
            if obj.timestamp.hour == 0:
                return timesince(obj.timestamp) + " ago"
            return timesince(obj.timestamp) + " ago"
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")


class TweetModelSerializer(serializers.ModelSerializer):
    user            = UserDisplaySerializer(read_only=True)
    date_display    = serializers.SerializerMethodField(source='get_date_display')
    parent          = ParentTweetModelSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'parent',
        ]

    def get_date_display(self, obj):
        if obj.timestamp.hour < 5:
            if obj.timestamp.hour == 0:
                return timesince(obj.timestamp) + " ago"
            return timesince(obj.timestamp) + " ago"
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")
