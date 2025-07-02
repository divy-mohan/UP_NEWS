from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'content']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'आपका नाम',
                'required': True
            }),
            'author_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'आपका ईमेल',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'आपकी टिप्पणी लिखें...',
                'required': True
            })
        }
        labels = {
            'author_name': 'नाम',
            'author_email': 'ईमेल',
            'content': 'टिप्पणी'
        }
