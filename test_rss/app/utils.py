import feedparser
from datetime import datetime
from django.utils.timezone import make_aware
from .models import Feed, FeedItem

def import_feed(feed_url):
    # Récupérer le flux
    parsed_feed = feedparser.parse(feed_url)

    # Créer ou mettre à jour le Feed
    feed, created = Feed.objects.get_or_create(
        url=feed_url,
        defaults={
            "title": parsed_feed.feed.get("title", ""),
            "description": parsed_feed.feed.get("description", ""),
        },
    )

    # Si on l’avait déjà, mettre à jour ses infos
    if not created:
        feed.title = parsed_feed.feed.get("title", feed.title)
        feed.description = parsed_feed.feed.get("description", feed.description)
    feed.save()

    # Parcourir les articles
    for entry in parsed_feed.entries:
        guid = entry.get("id") or entry.get("link")  # identifiant unique
        published = entry.get("published_parsed")

        # Convertir la date si elle existe
        published_date = None
        if published:
            published_date = make_aware(datetime(*published[:6]))

        # Créer ou ignorer si l'article existe déjà
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
