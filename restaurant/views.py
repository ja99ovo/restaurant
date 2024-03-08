from .models import tables, orders, OrderItem,Boisson,table_order
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

def table_list(request):
    table_list = tables.objects.all()
    for t in table_list:
        active_order=table_order.objects.filter(related_table_id=t.id,status='Active').first()
        t.active=table_order.objects.filter(related_table_id=t.id,status='Active').exists()
        t.active_id=active_order.related_order_id if t.active else None
    return render(request, 'restaurant/table_list.html', {'tables': table_list})

def boisson_list(request):
    boissons=Boisson.objects.all()
    return render(request, 'restaurant/add_order_item.html', {'boissons': boissons})

def table_detail(request, table_id):
    pass

def order_detail(request, table_id):
    table_order_list = table_order.objects.all()
    active_order=table_order_list.filter(related_table_id=table_id)
    return render(request, 'restaurant/table_list.html', {'id_order': active_order})




def cashier_summary(request):
    pass

def add_order_item(request):
    if request.method == 'POST':
        form =UserForm(request.POST)       
        if form.is_valid():
            pass
    return render(request, 'restaurant/add_order_item', {'form':form})

def order_detail(request, order_id):
    pass

def cashier_summary(request):
    pass

def clear_orders(request):
    pass
def clear_order(request, order_id):
    pass