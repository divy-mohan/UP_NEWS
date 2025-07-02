from django import forms
from .models import EventRegistration
from core.models import District

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['full_name', 'email', 'phone', 'age', 'gender', 'address', 'occupation', 'district']
        widgets = {
            'full_name': forms.TextInput(attrs={
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
                'placeholder': 'आपका मोबाइल नंबर',
                'required': True,
                'pattern': '[0-9]{10}'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'आपकी आयु',
                'min': 16,
                'max': 100,
                'required': True
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'आपका पूरा पता',
                'required': True
            }),
            'occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'आपका व्यवसाय/पेशा',
                'required': True
            }),
            'district': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            })
        }
        labels = {
            'full_name': 'पूरा नाम',
            'email': 'ईमेल',
            'phone': 'फोन नंबर',
            'age': 'आयु',
            'gender': 'लिंग',
            'address': 'पता',
            'occupation': 'व्यवसाय',
            'district': 'जिला'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.filter(is_active=True)
