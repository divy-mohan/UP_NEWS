from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('news/', include('news.urls')),
    path('events/', include('events.urls')),
    path('contact/', include('contact.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Also serve media files in production for Replit
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin customization
admin.site.site_header = "प्रांतीय युवा प्रकोष्ठ-उत्तर प्रदेश"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Welcome to Administration"
