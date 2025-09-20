from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('feed/<int:feed_id>/', views.feed_detail, name='feed_detail'),
    
    path('update-feed/<int:feed_id>/', views.update_feed, name='update_feed'),
    path('delete-feed/<int:feed_id>/', views.delete_feed, name='delete_feed'),
    path('refresh-all/', views.refresh_all_feeds, name='refresh_all_feeds'),
]