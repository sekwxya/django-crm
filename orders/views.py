from django.shortcuts import render

# Create your views here.

def order_list(request):
    return render(request, 'orders/order_list.html')

def order_create(request):
    return render(request, 'orders/order_create.html')

def order_detail(request, pk):
    return render(request, 'orders/order_detail.html')

def order_edit(request, pk):
    return render(request, 'orders/order_edit.html')

def order_delete(request, pk):
    return render(request, 'orders/order_delete.html')

def add_comment(request, pk):
    return render(request, 'orders/add_comment.html')

def generate_report(request):
    return render(request, 'orders/generate_report.html')
