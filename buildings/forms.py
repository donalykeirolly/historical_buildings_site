from django import forms
from .models import BuildingSuggestion

class BuildingSuggestionForm(forms.ModelForm):
    """Форма для предложения нового здания"""
    
    class Meta:
        model = BuildingSuggestion
        fields = ['name', 'address', 'city', 'description', 'suggested_by', 'suggested_email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Например: Эрмитаж'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Город, улица, дом'}),
            'city': forms.Select(attrs={'class': 'form-input'}),  # Выпадающий список
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5}),
            'suggested_by': forms.TextInput(attrs={'class': 'form-input'}),
            'suggested_email': forms.EmailInput(attrs={'class': 'form-input'}),
        }