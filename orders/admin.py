from django.contrib import admin
from .models import Order, OrderStatus, OrderComment

class OrderCommentInline(admin.TabularInline):
    """Встроенное отображение комментариев в админке заявки"""
    model = OrderComment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('author', 'text', 'created_at')

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'color')
    search_fields = ('name', 'description')
    list_filter = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'customer', 'manager', 'status', 'priority', 'created_at', 'deadline', 'is_overdue_display')
    list_filter = ('status', 'priority', 'created_at', 'deadline', 'manager')
    search_fields = ('number', 'title', 'description', 'customer__name', 'manager__username')
    readonly_fields = ('number', 'created_at', 'updated_at', 'completed_at')
    inlines = [OrderCommentInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('number', 'title', 'description', 'customer', 'manager', 'status', 'priority')
        }),
        ('Даты', {
            'fields': ('deadline', 'created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_overdue_display(self, obj):
        """Отображение просроченных заявок"""
        if obj.is_overdue:
            return '🔴 Просрочена'
        elif obj.deadline:
            days = obj.days_until_deadline
            if days and days <= 3:
                return f'🟡 Осталось {days} дн.'
        return '🟢 В норме'
    is_overdue_display.short_description = 'Статус дедлайна'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Только при создании
            obj.manager = request.user
        super().save_model(request, obj, form, change)

@admin.register(OrderComment)
class OrderCommentAdmin(admin.ModelAdmin):
    list_display = ('order', 'author', 'created_at', 'text_preview')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'order__number', 'author__username')
    readonly_fields = ('created_at',)
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст комментария'
