from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'आपका पूरा नाम',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'आपका ईमेल पता',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'आपका मोबाइल नंबर (वैकल्पिक)',
                'pattern': '[0-9]{10}'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'आपका संदेश यहाँ लिखें...',
                'required': True
            })
        }
        labels = {
            'name': 'नाम',
            'email': 'ईमेल',
            'phone': 'फोन नंबर',
            'subject': 'विषय',
            'message': 'संदेश'
        }
