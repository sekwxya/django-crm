from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Role(models.Model):
    """Модель ролей пользователей"""
    ADMIN = 'admin'
    MANAGER = 'manager'
    WAREHOUSE = 'warehouse'
    
    ROLE_CHOICES = [
        (ADMIN, 'Администратор'),
        (MANAGER, 'Менеджер'),
        (WAREHOUSE, 'Кладовщик'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
    
    def __str__(self):
        return self.get_name_display()

class UserProfile(models.Model):
    """Расширенная модель профиля пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f"{self.user.username} - {self.role.get_name_display() if self.role else 'Нет роли'}"
    
    @property
    def is_admin(self):
        return self.role and self.role.name == Role.ADMIN
    
    @property
    def is_manager(self):
        return self.role and self.role.name == Role.MANAGER
    
    @property
    def is_warehouse(self):
        return self.role and self.role.name == Role.WAREHOUSE

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Сигнал для автоматического создания профиля при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сигнал для сохранения профиля при сохранении пользователя"""
    instance.profile.save()
