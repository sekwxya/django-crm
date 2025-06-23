   # warehouse/views.py
from django.shortcuts import render

def product_list(request):
       return render(request, 'warehouse/product_list.html')

def product_create(request):
       return render(request, 'warehouse/product_create.html')

def product_detail(request, pk):
       return render(request, 'warehouse/product_detail.html')

def product_edit(request, pk):
       return render(request, 'warehouse/product_edit.html')

def product_delete(request, pk):
       return render(request, 'warehouse/product_delete.html')

def movement_list(request):
       return render(request, 'warehouse/movement_list.html')

def movement_create(request):
       return render(request, 'warehouse/movement_create.html')