from rest_framework import serializers
from django.utils.timesince import timesince
from datetime import datetime, timezone

from tweets.models import Tweet
from accounts.api.serializers import UserDisplaySerializer


def time_converter(time):
    minutes = abs(int(time / 60))
    hours = abs(int(time / 3600))
    return hours, minutes


class TweetModelSerializer(serializers.ModelSerializer):
    user            = UserDisplaySerializer(read_only=True)
    date_display    = serializers.SerializerMethodField(source='get_date_display')
    # timesince       = serializers.SerializerMethodField(source='get_timesince')

    class Meta:
        model = Tweet
        fields = [
            'user',
            'content',
            'timestamp',
            'date_display',
        ]

    def get_date_display(self, obj):
        time = (obj.timestamp - datetime.now(timezone.utc)).total_seconds()
        h, m = time_converter(time)
        if h < 5:
            if h == 0:
                return timesince(obj.timestamp) + " ago"
            return timesince(obj.timestamp) + " ago"
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    # def get_timesince(self, obj):
    #     return timesince(obj.timestamp) + " ago"
