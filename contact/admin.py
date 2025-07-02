from django.contrib import admin
from django.utils import timezone
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read', 'is_replied')
    list_filter = ('subject', 'is_read', 'is_replied', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read', 'is_replied')
    
    fieldsets = (
        ('संदेश जानकारी', {
            'fields': ('name', 'email', 'phone', 'subject', 'message', 'created_at')
        }),
        ('स्थिति', {
            'fields': ('is_read', 'is_replied')
        }),
        ('जवाब', {
            'fields': ('reply_message', 'replied_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Selected messages को read के रूप में mark करें"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Selected messages को unread के रूप में mark करें"
    
    def save_model(self, request, obj, form, change):
        if obj.reply_message and not obj.replied_at:
            obj.replied_at = timezone.now()
            obj.is_replied = True
        super().save_model(request, obj, form, change)
