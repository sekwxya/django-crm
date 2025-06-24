from django import forms
from .models import Order, OrderComment

class OrderForm(forms.ModelForm):
    """Форма для создания и редактирования заявки"""
    
    class Meta:
        model = Order
        fields = ['customer', 'title', 'description', 'priority', 'deadline']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }

class OrderEditForm(forms.ModelForm):
    """Форма для редактирования заявки (включая статус и менеджера)"""
    
    class Meta:
        model = Order
        fields = ['customer', 'title', 'description', 'priority', 'deadline', 'status', 'manager']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
        }

class OrderCommentForm(forms.ModelForm):
    """Форма для добавления комментария к заявке"""
    
    class Meta:
        model = OrderComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите ваш комментарий...'
            }),
        }
        labels = {
            'text': 'Комментарий'
        } 