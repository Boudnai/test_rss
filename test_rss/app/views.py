from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import feedparser
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Feed, FeedItem
from .serializers import FeedSerializer, FeedItemSerializer
from .utils import import_feed 

# Create your views here.

RSS_URLS = [
    "https://www.lemonde.fr/rss/une.xml",
    "https://www.lefigaro.fr/rss/figaro_actualites.xml",
    "https://feeds.bbci.co.uk/news/world/europe/rss.xml"
    ]

class ArticlesView(APIView):
    def get(self, request):
        articles = []

        for url in RSS_URLS:
            flux = feedparser.parse(url)
            for entry in flux.entries:
                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": getattr(entry, "summary", ""),
                    "published": getattr(entry, "published", None),
                    "source": flux.feed.title
                })

        return Response(articles)


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    # Optionnel : récupérer les articles d’un flux spécifique
    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        feed = self.get_object()
        items = feed.items.all()
        serializer = FeedItemSerializer(items, many=True)
        return Response(serializer.data)

# Pour les articles (optionnel si besoin de endpoints séparés)
class FeedItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeedItem.objects.all()
    serializer_class = FeedItemSerializer


def index(request):
    return render(request, "index.html")