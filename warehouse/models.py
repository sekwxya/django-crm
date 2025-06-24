from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """Модель товара на складе"""
    name = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} (остаток: {self.quantity})"
    
    @property
    def total_value(self):
        """Общая стоимость товара на складе"""
        if self.price is None:
            return 0
        return self.quantity * self.price

class Movement(models.Model):
    """Модель движения товаров (приход/расход)"""
    MOVEMENT_TYPES = [
        ('in', 'Приход'),
        ('out', 'Расход'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES, verbose_name='Тип движения')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата движения')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    
    class Meta:
        verbose_name = 'Движение товара'
        verbose_name_plural = 'Движения товаров'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.get_movement_type_display()} {self.product.name} - {self.quantity} шт."
    
    def save(self, *args, **kwargs):
        """Обновляем количество товара при сохранении движения"""
        if not self.pk:  # Только при создании нового движения
            if self.movement_type == 'in':
                self.product.quantity += self.quantity
            else:  # 'out'
                if self.product.quantity >= self.quantity:
                    self.product.quantity -= self.quantity
                else:
                    raise ValueError("Недостаточно товара на складе")
            self.product.save()
        super().save(*args, **kwargs)
