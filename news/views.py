from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import News, Comment
from .forms import CommentForm
from core.models import Category, District

def news_list(request):
    """News list view with filtering and search"""
    news_queryset = News.objects.filter(is_published=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        news_queryset = news_queryset.filter(
            Q(title__icontains=search_query) |
            Q(summary__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Category filter
    selected_category = request.GET.get('category', '')
    if selected_category:
        news_queryset = news_queryset.filter(category_id=selected_category)
    
    # District filter
    selected_district = request.GET.get('district', '')
    if selected_district:
        news_queryset = news_queryset.filter(district_id=selected_district)
    
    # Pagination
    paginator = Paginator(news_queryset, 12)  # 12 news per page
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    # Get filter options
    categories = Category.objects.filter(is_active=True)
    districts = District.objects.filter(is_active=True)
    
    context = {
        'news': news,
        'categories': categories,
        'districts': districts,
        'search': search_query,
        'selected_category': selected_category,
        'selected_district': selected_district,
    }
    return render(request, 'news/list.html', context)

def news_detail(request, pk):
    """News detail view with comments"""
    news = get_object_or_404(News, pk=pk, is_published=True)
    
    # Increment view count
    news.increment_views()
    
    # Get approved comments
    comments = news.comments.filter(is_approved=True)
    
    # Comment form
    comment_form = CommentForm()
    
    # Related news (same category, excluding current)
    related_news_list = News.objects.filter(
        category=news.category,
        is_published=True
    ).exclude(pk=pk)[:5]
    
    # Popular news (most views)
    popular_news_list = News.objects.filter(
        is_published=True
    ).order_by('-views_count')[:5]
    
    # Categories with news count
    categories = Category.objects.filter(is_active=True)
    for category in categories:
        category.news_count = News.objects.filter(category=category, is_published=True).count()
    
    context = {
        'news': news,
        'comments': comments,
        'comment_form': comment_form,
        'related_news_list': related_news_list,
        'popular_news_list': popular_news_list,
        'categories': categories,
    }
    return render(request, 'news/detail.html', context)

def add_comment(request, pk):
    """Add comment to news"""
    news = get_object_or_404(News, pk=pk, is_published=True)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.save()
            messages.success(request, 'आपकी टिप्पणी सफलतापूर्वक जोड़ी गई!')
        else:
            messages.error(request, 'कृपया सभी फील्ड सही तरीके से भरें।')
    
    return redirect('news:detail', pk=pk)

@require_POST
@csrf_exempt
def like_news(request, pk):
    """AJAX view to like news"""
    news = get_object_or_404(News, pk=pk)
    news.likes_count += 1
    news.save(update_fields=['likes_count'])
    
    return JsonResponse({
        'status': 'success',
        'likes_count': news.likes_count
    })
