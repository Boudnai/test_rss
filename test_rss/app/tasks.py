from django_q.tasks import schedule
from django_q.models import Schedule
from .utils import import_feed

# Liste de tous tes flux
FLUX_URLS = [
    "https://www.lemonde.fr/rss/une.xml",
    "http://feeds.bbci.co.uk/news/technology/rss.xml"
]

def update_all_feeds():
    for url in FLUX_URLS:
        import_feed(url)
