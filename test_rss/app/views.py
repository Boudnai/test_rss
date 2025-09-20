from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Feed, FeedItem
from .utils import import_feed

def index(request):
    """Page d'accueil avec la liste des flux"""
    feeds = Feed.objects.all().order_by('-created_at')
    
    # Recherche simple
    search = request.GET.get('search', '')
    if search:
        feeds = feeds.filter(
            Q(title__icontains=search) | Q(url__icontains=search)
        )
    
    context = {
        'feeds': feeds,
        'search': search,
        'total_feeds': Feed.objects.count(),
        'total_articles': FeedItem.objects.count(),
    }
    return render(request, 'app/index.html', context)

def feed_detail(request, feed_id):
    """Affichage des articles d'un flux spécifique"""
    feed = get_object_or_404(Feed, id=feed_id)
    articles = feed.items.all().order_by('-published_date')
    
    # Recherche dans les articles
    search = request.GET.get('search', '')
    if search:
        articles = articles.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'feed': feed,
        'articles': page_obj,
        'search': search,
    }
    return render(request, 'app/feed_detail.html', context)

def update_feed(request, feed_id):
    """Mettre à jour un flux (re-importer les articles)"""
    feed = get_object_or_404(Feed, id=feed_id)
    
    try:
        import_feed(feed.url)
        messages.success(request, f'Flux "{feed.title}" mis à jour avec succès!')
    except Exception as e:
        messages.error(request, f'Erreur lors de la mise à jour: {str(e)}')
    
    return redirect('feed_detail', feed_id=feed.id)

def delete_feed(request, feed_id):
    """Supprimer un flux"""
    feed = get_object_or_404(Feed, id=feed_id)
    
    if request.method == 'POST':
        feed_title = feed.title
        feed.delete()
        messages.success(request, f'Flux "{feed_title}" supprimé avec succès!')
        return redirect('index')
    
    return render(request, 'app/delete_feed.html', {'feed': feed})

def refresh_all_feeds(request):
    """Actualiser tous les flux"""
    feeds = Feed.objects.all()
    updated_count = 0
    error_count = 0
    
    for feed in feeds:
        try:
            import_feed(feed.url)
            updated_count += 1
        except Exception as e:
            error_count += 1
            print(f"Erreur pour {feed.url}: {e}")
    
    if updated_count > 0:
        messages.success(request, f'{updated_count} flux mis à jour avec succès!')
    if error_count > 0:
        messages.warning(request, f'{error_count} flux ont échoué lors de la mise à jour.')
    
    return redirect('index')