from rest_framework import serializers

from tweets.models import Tweet
from accounts.api.serializers import UserDisplaySerializer


class ParentTweetModelSerializer(serializers.ModelSerializer):
    user            = UserDisplaySerializer(read_only=True)
    date_display    = serializers.SerializerMethodField(source='get_date_display')
    likes           = serializers.SerializerMethodField(source='get_likes')
    did_liked       = serializers.SerializerMethodField(source='get_did_liked')

    class Meta:
        model = Tweet
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'likes',
            'did_liked',
        ]

    def get_did_liked(self, obj):
        user = self.context.get('user')
        if user in obj.liked.all():
            return True
        return False

    def get_likes(self, obj):
        return obj.liked.all().count()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%d %B, %Y")


class TweetModelSerializer(serializers.ModelSerializer):
    user            = UserDisplaySerializer(read_only=True)
    date_display    = serializers.SerializerMethodField(source='get_date_display')
    parent          = ParentTweetModelSerializer(read_only=True)
    likes           = serializers.SerializerMethodField(source='get_likes')
    did_liked       = serializers.SerializerMethodField(source='get_did_liked')

    class Meta:
        model = Tweet
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'parent',
            'likes',
            'did_liked',
        ]

    def get_did_liked(self, obj):
        user = self.context.get('user')
        if user in obj.liked.all():
            return True
        return False

    def get_likes(self, obj):
        return obj.liked.all().count()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%d %B, %Y")
