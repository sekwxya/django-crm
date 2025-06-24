from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Customer
from .forms import CustomerForm

# Create your views here.

@login_required
def customer_list(request):
    """Список всех клиентов"""
    customers = Customer.objects.all()
    
    # Поиск
    search = request.GET.get('search')
    if search:
        customers = customers.filter(
            Q(name__icontains=search) |
            Q(contact_person__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(address__icontains=search)
        )
    
    # Статистика
    total_customers = customers.count()
    active_customers = customers.count()  # Все клиенты считаются активными
    
    # Пагинация
    paginator = Paginator(customers, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'total_customers': total_customers,
        'active_customers': active_customers,
    }
    return render(request, 'customers/customer_list.html', context)

@login_required
def customer_create(request):
    """Создание нового клиента"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Клиент успешно создан!')
            return redirect('customers:customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'customers/customer_create.html', {'form': form})

@login_required
def customer_detail(request, pk):
    """Детальная информация о клиенте"""
    customer = get_object_or_404(Customer, pk=pk)
    
    # Получаем заявки клиента (если есть модуль orders)
    try:
        from orders.models import Order
        orders = Order.objects.filter(customer=customer)[:5]  # Последние 5 заявок
    except ImportError:
        orders = []
    
    context = {
        'customer': customer,
        'orders': orders,
    }
    return render(request, 'customers/customer_detail.html', context)

@login_required
def customer_edit(request, pk):
    """Редактирование клиента"""
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Клиент успешно обновлен!')
            return redirect('customers:customer_detail', pk=pk)
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'customers/customer_edit.html', {'form': form, 'customer': customer})

@login_required
def customer_delete(request, pk):
    """Удаление клиента"""
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Клиент успешно удален!')
        return redirect('customers:customer_list')
    
    return render(request, 'customers/customer_delete.html', {'customer': customer})
