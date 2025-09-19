from django.contrib import admin
from .models import Feed, FeedItem

# Register your models here.

admin.site.register(Feed)
admin.site.register(FeedItem)