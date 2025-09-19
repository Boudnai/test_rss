from django.db import models

# Create your models here.

class Feed(models.Model):
    url = models.URLField(unique=True)  
    title = models.CharField(max_length=255, blank=True, null=True) 
    description = models.TextField(blank=True, null=True)  
    last_entry = models.DateTimeField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.title or self.url


class FeedItem(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="items")  
    title = models.CharField(max_length=255)
    link = models.URLField()
    description = models.TextField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    guid = models.CharField(max_length=255, unique=True) 

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
