from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer

class OrderStatus(models.Model):
    """Модель статусов заявок"""
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (NEW, 'Новая'),
        (IN_PROGRESS, 'В работе'),
        (COMPLETED, 'Выполнена'),
        (REJECTED, 'Отклонена'),
    ]
    
    name = models.CharField(max_length=20, choices=STATUS_CHOICES, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Цвет в формате #RRGGBB')
    
    class Meta:
        verbose_name = 'Статус заявки'
        verbose_name_plural = 'Статусы заявок'
    
    def __str__(self):
        return self.get_name_display()

class Order(models.Model):
    """Модель заявки"""
    number = models.CharField(max_length=20, unique=True, verbose_name='Номер заявки')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ответственный менеджер')
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, verbose_name='Статус')
    title = models.CharField(max_length=200, verbose_name='Заголовок заявки')
    description = models.TextField(verbose_name='Описание')
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('urgent', 'Срочный'),
    ], default='medium', verbose_name='Приоритет')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='Срок выполнения')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата выполнения')
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заявка #{self.number} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Автоматически генерируем номер заявки при создании
        if not self.pk and not self.number:
            last_order = Order.objects.order_by('-id').first()
            if last_order:
                last_number = int(last_order.number.replace('ORD-', ''))
                self.number = f"ORD-{last_number + 1:06d}"
            else:
                self.number = "ORD-000001"
        
        # Автоматически устанавливаем дату выполнения при изменении статуса на "Выполнена"
        if self.status and self.status.name == OrderStatus.COMPLETED and not self.completed_at:
            from django.utils import timezone
            self.completed_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        """Проверяет, просрочена ли заявка"""
        if self.deadline and self.status.name not in [OrderStatus.COMPLETED, OrderStatus.REJECTED]:
            from django.utils import timezone
            return timezone.now() > self.deadline
        return False
    
    @property
    def days_until_deadline(self):
        """Количество дней до дедлайна"""
        if self.deadline:
            from django.utils import timezone
            delta = self.deadline - timezone.now()
            return delta.days
        return None

class OrderComment(models.Model):
    """Модель комментария к заявке"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='comments', verbose_name='Заявка')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Комментарий к заявке'
        verbose_name_plural = 'Комментарии к заявкам'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Комментарий к заявке #{self.order.number} от {self.author.username}"
