from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    """Форма для создания и редактирования клиента"""
    
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'contact_person', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        } 