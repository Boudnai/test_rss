from . import views
from .views import ArticlesView, index
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeedViewSet, FeedItemViewSet

router = DefaultRouter()
router.register(r'feeds', FeedViewSet)
router.register(r'items', FeedItemViewSet)  # optionnel

urlpatterns = [
    path('', index, name = 'index'),
    path("articles/", ArticlesView.as_view(), name="articles"),
]