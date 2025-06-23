from django.shortcuts import render

# Create your views here.

def customer_list(request):
    return render(request, 'customers/customer_list.html')

def customer_create(request):
    return render(request, 'customers/customer_create.html')

def customer_detail(request, pk):
    return render(request, 'customers/customer_detail.html')

def customer_edit(request, pk):
    return render(request, 'customers/customer_edit.html')

def customer_delete(request, pk):
    return render(request, 'customers/customer_delete.html')
