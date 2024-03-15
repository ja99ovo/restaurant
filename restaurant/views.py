from .models import tables, orders, OrderItem,Boisson,table_order
from django.shortcuts import render, redirect, get_object_or_404
from .forms import New_order_form

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


def table_detail(request, table_id):
    pass

def order_detail(request, table_id):
    table_order_list = table_order.objects.all()
    active_order=table_order_list.filter(related_table_id=table_id)
    return render(request, 'restaurant/table_list.html', {'id_order': active_order})




def cashier_summary(request):
    pass

def add_order_item(request):
    boissons=Boisson.objects.all()
    table_id = request.GET.get('table_id')
    table_this=tables.objects.get(id=table_id)
    if request.method == 'POST':
        form =New_order_form(request.POST)
        
        if form.is_valid():
            adults=form.cleaned_data.get('adults')
            toddlers=form.cleaned_data.get('toddlers')
            kids=form.cleaned_data.get('kids')
            
                
            new_order=orders(adults=adults,kids=kids,toddlers=toddlers)
            new_order.save()
            new_table_order=table_order(status='Active',related_order=new_order,related_table=table_this)
            new_table_order.save()
            for b in boissons:
                quantity=form.cleaned_data.get(f'boisson_{b.name}')
                new_order_item=OrderItem(quantity=quantity,boisson=b,order=new_order)
                new_order_item.save()
            return HttpResponseRedirect('')
        else:
            print("not valid")
    else:
        form = New_order_form()
    return render(request, 'restaurant/add_order_item.html', {'form':form,'boissons': boissons})

def order_detail(request, order_id):
    pass

def cashier_summary(request):
    pass

def clear_orders(request):
    pass
def clear_order(request, order_id):
    pass