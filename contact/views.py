from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def contact_view(request):
    """Contact form view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email notification to admin
            try:
                admin_subject = f"नया संपर्क संदेश - {contact_message.get_subject_display()}"
                admin_message = f"""
                नया संपर्क संदेश प्राप्त हुआ है:
                
                नाम: {contact_message.name}
                ईमेल: {contact_message.email}
                फोन: {contact_message.phone or 'नहीं दिया गया'}
                विषय: {contact_message.get_subject_display()}
                
                संदेश:
                {contact_message.message}
                
                समय: {contact_message.created_at.strftime('%d/%m/%Y %H:%M')}
                """
                
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['admin@pranteeyyuva.org'],  # Admin email
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Failed to send admin notification: {e}")
            
            # Send confirmation email to user
            try:
                user_subject = "आपका संदेश प्राप्त हुआ - प्रांतीय युवा प्रकोष्ठ"
                user_message = f"""
                प्रिय {contact_message.name},
                
                आपका संदेश हमें प्राप्त हो गया है। हम जल्द ही आपसे संपर्क करेंगे।
                
                आपका संदेश:
                {contact_message.message}
                
                धन्यवाद,
                प्रांतीय युवा प्रकोष्ठ-उत्तर प्रदेश
                """
                
                send_mail(
                    user_subject,
                    user_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [contact_message.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Failed to send user confirmation: {e}")
            
            messages.success(request, 'आपका संदेश सफलतापूर्वक भेज दिया गया है! हम जल्द ही आपसे संपर्क करेंगे।')
            return redirect('contact:contact')
        else:
            messages.error(request, 'कृपया सभी आवश्यक फील्ड सही तरीके से भरें।')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'contact/contact.html', context)
