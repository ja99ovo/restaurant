from .models import tables, orders, OrderItem,Boisson,table_order
from django.shortcuts import render, redirect, get_object_or_404
from .forms import New_order_form, Change_order_form
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

def table_list(request):
    table_list = tables.objects.all()
    for t in table_list:
        order_active=table_order.objects.filter(related_table_id=t.id,status='Active').first()
        t.active=table_order.objects.filter(related_table_id=t.id,status='Active').exists()
        t.active_id=order_active.related_order_id if t.active else None
    return render(request, 'restaurant/table_list.html', {'tables': table_list})

def add_table(request):
    if request.method == 'POST':
        # 在这里处理添加新桌子的逻辑
        new_table = tables()  # 假设 'tables' 是你的桌子模型
        new_table.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def table_detail(request, table_id):
    pass

def order_detail(request):
    table_id = request.GET.get('table_id')
    boissons=Boisson.objects.all()
    table_obj=tables.objects.get(id=table_id)
    
    order_id=table_order.objects.filter(related_table_id=table_id,status='Active').values_list(
            'related_order_id',flat=True).first()
    order_obj=orders.objects.filter(id=order_id).first()
    boisson_ordered=OrderItem.objects.filter(order_id=order_id).all()
    if request.method == 'POST':
        form = Change_order_form(request.POST)
        if form.is_valid():
            adults=form.cleaned_data.get('adults')
            toddlers=form.cleaned_data.get('toddlers')
            kids=form.cleaned_data.get('kids')
            order_obj.adults=adults
            order_obj.kids=kids
            order_obj.toddlers=toddlers
            order_obj.save()
            
        for b in boissons:
            quantity=form.cleaned_data.get(f'boisson_{b.name}')
            b_old=boisson_ordered.filter(boisson=b).all().first()
            b_old.quantity=quantity
            b_old.save()
            
    form = Change_order_form()
    for b in boissons:
        b.quantity = boisson_ordered.filter(boisson_id=b.id).values_list("quantity",flat=True).first() if boisson_ordered.filter(boisson_id=b.id).exists() else 0
    return render(request, 'restaurant/order_detail.html', {
        'adults':order_obj.adults,
        'kids':order_obj.kids,
        'toddlers':order_obj.toddlers,
        'form':form,
        'boissons': boissons
    })


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
                
            #重定向到订单修改页面
            new_form=Change_order_form()
            boisson_ordered=OrderItem.objects.filter(order=new_order).all()
            for b in boissons:
                b.quantity = boisson_ordered.filter(boisson_id=b.id).values_list("quantity",flat=True).first() if boisson_ordered.filter(boisson_id=b.id).exists() else 0
            return render(request, 'restaurant/order_detail.html', {
                'adults':adults,
                'kids':kids,
                'toddlers':toddlers,
                'form':new_form,
                'boissons': boissons
            })
        else:
            print("not valid")
    else:
        form = New_order_form()
    return render(request, 'restaurant/add_order_item.html', {'form':form,'boissons': boissons})


def cashier_summary(request):
    pass

def clear_orders(request):
    pass
def clear_order(request, order_id):
    pass