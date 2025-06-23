from django.urls import path
from . import views

app_name = 'warehouse'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('movement/', views.movement_list, name='movement_list'),
    path('movement/create/', views.movement_create, name='movement_create'),
] 