from django.contrib import admin
from django import forms
from .models import Product, Movement

class MovementAdminForm(forms.ModelForm):
    """Форма для админки с валидацией движения товаров"""
    
    class Meta:
        model = Movement
        fields = '__all__'
    
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

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'total_value', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'total_value')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'price')
        }),
        ('Остатки', {
            'fields': ('quantity', 'total_value')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    form = MovementAdminForm
    list_display = ('product', 'movement_type', 'quantity', 'date', 'user')
    list_filter = ('movement_type', 'date', 'product')
    search_fields = ('product__name', 'notes')
    readonly_fields = ('date',)
    
    fieldsets = (
        ('Движение', {
            'fields': ('product', 'movement_type', 'quantity')
        }),
        ('Дополнительно', {
            'fields': ('user', 'notes', 'date')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Только при создании
            obj.user = request.user
        super().save_model(request, obj, form, change)
