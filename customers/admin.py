from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'contact_person', 'email', 'phone', 'address')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'contact_person', 'email', 'phone')
        }),
        ('Адрес и примечания', {
            'fields': ('address', 'notes')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
