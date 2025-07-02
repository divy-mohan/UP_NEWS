from django.shortcuts import render
from django.core.paginator import Paginator
from news.models import News
from events.models import Event
from core.models import SiteSettings, Banner

def home(request):
    """Home page view with featured content"""
    # Get featured news (latest 6)
    featured_news = News.objects.filter(
        is_featured=True,
        is_published=True
    ).order_by('-date_posted')[:6]
    
    # Get upcoming events (next 6)
    upcoming_events = Event.objects.filter(
        is_published=True
    ).order_by('event_date')[:6]
    
    # Get active banners
    banners = Banner.objects.filter(is_active=True).order_by('order')
    
    context = {
        'featured_news': featured_news,
        'upcoming_events': upcoming_events,
        'banners': banners,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'core/about.html', context)
