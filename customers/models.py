from django.db import models

# Create your models here.

class Customer(models.Model):
    """Модель клиента"""
    name = models.CharField(max_length=200, verbose_name='Наименование')
    email = models.EmailField(blank=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    address = models.TextField(blank=True, verbose_name='Адрес')
    contact_person = models.CharField(max_length=100, blank=True, verbose_name='Контактное лицо')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['name']
    
    def __str__(self):
        return self.name
