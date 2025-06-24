from django import forms
from .models import Product, Movement

class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования товара"""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class MovementForm(forms.ModelForm):
    """Форма для создания движения товара"""
    
    class Meta:
        model = Movement
        fields = ['product', 'movement_type', 'quantity', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'movement_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        movement_type = cleaned_data.get('movement_type')
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        
        if movement_type == 'out' and product and quantity:
            if product.quantity < quantity:
                raise forms.ValidationError(
                    f"Недостаточно товара на складе. Доступно: {product.quantity} шт."
                )
        
        return cleaned_data 