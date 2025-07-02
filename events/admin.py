from django.contrib import admin
from .models import Event, EventRegistration, EventImage

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1

class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ('registration_number', 'registration_date')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'district', 'event_date', 'registered_count', 'available_spots', 'is_published')
    list_filter = ('category', 'district', 'is_published', 'is_featured', 'event_date')
    search_fields = ('title', 'description', 'venue')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EventImageInline, EventRegistrationInline]
    list_editable = ('is_published',)
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('मुख्य जानकारी', {
            'fields': ('title', 'slug', 'description', 'venue')
        }),
        ('वर्गीकरण', {
            'fields': ('category', 'district')
        }),
        ('तिथि और समय', {
            'fields': ('event_date', 'registration_deadline')
        }),
        ('पंजीकरण सेटिंग्स', {
            'fields': ('registration_fee', 'max_participants')
        }),
        ('प्रकाशन सेटिंग्स', {
            'fields': ('is_published', 'is_featured')
        })
    )

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'full_name', 'event', 'email', 'phone', 'registration_date', 'is_confirmed', 'payment_status')
    list_filter = ('event', 'district', 'gender', 'is_confirmed', 'payment_status', 'registration_date')
    search_fields = ('full_name', 'email', 'phone', 'registration_number')
    readonly_fields = ('registration_number', 'registration_date')
    list_editable = ('is_confirmed', 'payment_status')
    
    fieldsets = (
        ('पंजीकरण जानकारी', {
            'fields': ('registration_number', 'event', 'registration_date')
        }),
        ('व्यक्तिगत जानकारी', {
            'fields': ('full_name', 'email', 'phone', 'age', 'gender', 'address', 'occupation', 'district')
        }),
        ('स्थिति', {
            'fields': ('is_confirmed', 'payment_status')
        })
    )

@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ('event', 'caption', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('event__title', 'caption')
