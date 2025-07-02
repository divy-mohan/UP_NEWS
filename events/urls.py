from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.events_list, name='list'),
    path('<int:pk>/', views.event_detail, name='detail'),
    path('<int:pk>/register/', views.event_register, name='register_event'),
    path('register/', views.event_register, name='register'),
    path('success/<int:registration_id>/', views.registration_success, name='success'),
    path('download-id/<int:registration_id>/', views.download_id_card, name='download_id_card'),
    path('email-id/<int:registration_id>/', views.email_id_card, name='email_id_card'),
]
