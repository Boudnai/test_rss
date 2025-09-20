import feedparser
from datetime import datetime
from django.utils.timezone import make_aware
from .models import Feed, FeedItem

def import_feed(feed_url):
    parsed_feed = feedparser.parse(feed_url)

    feed, created = Feed.objects.get_or_create(
        url=feed_url,
        defaults={
            "title": parsed_feed.feed.get("title", ""),
            "description": parsed_feed.feed.get("description", ""),
        },
    )

    if not created:
        feed.title = parsed_feed.feed.get("title", feed.title)
        feed.description = parsed_feed.feed.get("description", feed.description)
    feed.save()

    for entry in parsed_feed.entries:
        guid = entry.get("id") or entry.get("link") 
        published = entry.get("published_parsed")

        published_date = None
        if published:
            published_date = make_aware(datetime(*published[:6]))

        FeedItem.objects.get_or_create(
            guid=guid,
            defaults={
                "feed": feed,
                "title": entry.get("title", "Sans titre"),
                "link": entry.get("link", ""),
                "description": entry.get("summary", ""),
                "published_date": published_date,
            },
        )

    return feed