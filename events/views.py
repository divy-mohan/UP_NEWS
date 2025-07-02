from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from .models import Event, EventRegistration
from .forms import EventRegistrationForm
from .utils import generate_id_card, send_id_card_email
from core.models import Category, District

def events_list(request):
    """Events list view with filtering"""
    events_queryset = Event.objects.filter(is_published=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        events_queryset = events_queryset.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(venue__icontains=search_query)
        )
    
    # Category filter
    selected_category = request.GET.get('category', '')
    if selected_category:
        events_queryset = events_queryset.filter(category_id=selected_category)
    
    # District filter
    selected_district = request.GET.get('district', '')
    if selected_district:
        events_queryset = events_queryset.filter(district_id=selected_district)
    
    # Pagination
    paginator = Paginator(events_queryset, 12)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    
    # Get filter options
    categories = Category.objects.filter(is_active=True)
    districts = District.objects.filter(is_active=True)
    
    context = {
        'events': events,
        'categories': categories,
        'districts': districts,
        'search': search_query,
        'selected_category': selected_category,
        'selected_district': selected_district,
    }
    return render(request, 'events/list.html', context)

def event_detail(request, pk):
    """Event detail view"""
    event = get_object_or_404(Event, pk=pk, is_published=True)
    
    # Check if registration is still open
    registration_open = timezone.now() < event.registration_deadline
    spots_available = event.available_spots > 0
    
    context = {
        'event': event,
        'registration_open': registration_open,
        'spots_available': spots_available,
    }
    return render(request, 'events/detail.html', context)

def event_register(request, pk=None):
    """Event registration view"""
    event = None
    if pk:
        event = get_object_or_404(Event, pk=pk, is_published=True)
        
        # Check if registration is closed
        if timezone.now() >= event.registration_deadline:
            messages.error(request, 'इस कार्यक्रम के लिए पंजीकरण बंद हो गया है।')
            return redirect('events:detail', pk=pk)
        
        # Check if spots are available
        if event.available_spots <= 0:
            messages.error(request, 'इस कार्यक्रम के लिए सभी स्थान भर गए हैं।')
            return redirect('events:detail', pk=pk)
    
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            if event:
                registration.event = event
            else:
                # General registration - assign to a default event or handle differently
                latest_event = Event.objects.filter(is_published=True).first()
                if latest_event:
                    registration.event = latest_event
                else:
                    messages.error(request, 'कोई सक्रिय कार्यक्रम उपलब्ध नहीं है।')
                    return redirect('core:home')
            
            registration.save()
            messages.success(request, 'आपका पंजीकरण सफल रहा!')
            return redirect('events:success', registration_id=registration.id)
        else:
            messages.error(request, 'कृपया सभी फील्ड सही तरीके से भरें।')
    else:
        form = EventRegistrationForm()
    
    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'events/register_form.html', context)

def registration_success(request, registration_id):
    """Registration success view"""
    registration = get_object_or_404(EventRegistration, id=registration_id)
    
    context = {
        'registration': registration,
    }
    return render(request, 'events/success.html', context)

def download_id_card(request, registration_id):
    """Download ID card PDF"""
    registration = get_object_or_404(EventRegistration, id=registration_id)
    
    # Generate PDF
    buffer = generate_id_card(registration)
    
    # Create response
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ID_Card_{registration.registration_number}.pdf"'
    
    return response

def email_id_card(request, registration_id):
    """Email ID card to participant"""
    registration = get_object_or_404(EventRegistration, id=registration_id)
    
    success = send_id_card_email(registration)
    
    if success:
        messages.success(request, 'ID कार्ड आपके ईमेल पर भेज दिया गया है!')
    else:
        messages.error(request, 'ईमेल भेजने में समस्या हुई। कृपया बाद में कोशिश करें।')
    
    return redirect('events:success', registration_id=registration_id)
