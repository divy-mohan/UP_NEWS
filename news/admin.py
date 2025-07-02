from django.contrib import admin
from .models import News, NewsImage, Comment

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'district', 'author', 'date_posted', 'is_published', 'is_featured', 'views_count')
    list_filter = ('category', 'district', 'is_published', 'is_featured', 'date_posted')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [NewsImageInline]
    list_editable = ('is_published', 'is_featured')
    date_hierarchy = 'date_posted'
    
    fieldsets = (
        ('मुख्य जानकारी', {
            'fields': ('title', 'slug', 'summary', 'content')
        }),
        ('वर्गीकरण', {
            'fields': ('category', 'district', 'author')
        }),
        ('प्रकाशन सेटिंग्स', {
            'fields': ('is_published', 'is_featured')
        }),
        ('आंकड़े', {
            'fields': ('views_count', 'likes_count'),
            'classes': ('collapse',)
        })
    )

@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ('news', 'caption', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('news__title', 'caption')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'news', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('author_name', 'author_email', 'content')
    list_editable = ('is_approved',)
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Selected comments को approve करें"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "Selected comments को disapprove करें"
