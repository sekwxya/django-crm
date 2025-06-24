   # warehouse/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, Movement
from .forms import ProductForm, MovementForm

@login_required
def product_list(request):
    """Список всех товаров"""
    products = Product.objects.all()
    
    # Поиск
    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)
    
    # Пагинация
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
    }
    return render(request, 'warehouse/product_list.html', context)

@login_required
def product_create(request):
    """Создание нового товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно создан!')
            return redirect('warehouse:product_list')
    else:
        form = ProductForm()
    
    return render(request, 'warehouse/product_create.html', {'form': form})

@login_required
def product_detail(request, pk):
    """Детальная информация о товаре"""
    product = get_object_or_404(Product, pk=pk)
    movements = Movement.objects.filter(product=product)[:10]  # Последние 10 движений
    
    context = {
        'product': product,
        'movements': movements,
    }
    return render(request, 'warehouse/product_detail.html', context)

@login_required
def product_edit(request, pk):
    """Редактирование товара"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно обновлен!')
            return redirect('warehouse:product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'warehouse/product_edit.html', {'form': form, 'product': product})

@login_required
def product_delete(request, pk):
    """Удаление товара"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар успешно удален!')
        return redirect('warehouse:product_list')
    
    return render(request, 'warehouse/product_delete.html', {'product': product})

@login_required
def movement_list(request):
    """Список всех движений товаров"""
    movements = Movement.objects.select_related('product', 'user').all()
    
    # Фильтрация
    movement_type = request.GET.get('type')
    if movement_type:
        movements = movements.filter(movement_type=movement_type)
    
    # Пагинация
    paginator = Paginator(movements, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'movement_type': movement_type,
    }
    return render(request, 'warehouse/movement_list.html', context)

@login_required
def movement_create(request):
    """Создание нового движения товара"""
    if request.method == 'POST':
        form = MovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.user = request.user
            movement.save()
            messages.success(request, 'Движение товара успешно создано!')
            return redirect('warehouse:movement_list')
    else:
        form = MovementForm()
    
    return render(request, 'warehouse/movement_create.html', {'form': form})