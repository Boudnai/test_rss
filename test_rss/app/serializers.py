from rest_framework import serializers
from .models import Feed, FeedItem

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ['id', 'url', 'title', 'description', 'last_entry']

class FeedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedItem
        fields = ['id', 'feed', 'title', 'link', 'description', 'published_date', 'guid']
