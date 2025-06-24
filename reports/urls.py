from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('orders/', views.report_orders, name='report_orders'),
] 