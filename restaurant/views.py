from .models import Table, Order, Order_item,Boisson, Category
from django.shortcuts import render, redirect, get_object_or_404
from .forms import New_order_form, login_form
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from decimal import Decimal


@login_required(redirect_field_name="login_view")
def table_list(request):
    table_list = Table.objects.all()
    for t in table_list:
        order_active=t.orders.all().filter(status='Active').first()
        t.active=order_active.id if order_active else None
    return render(request, 'restaurant/table_list.html', {'tables': table_list})

def add_table(request):
    if request.method == 'POST':
        # 在这里处理添加新桌子的逻辑
        new_table = Table()  # 假设 'tables' 是你的桌子模型
        new_table.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def base(request):
    pass

@login_required(redirect_field_name="login_view")
def table_detail(request, table_id):
    pass


@login_required(redirect_field_name="login")
def add_order_item(request):
    table_id = request.GET.get('table_id')
    table_this=Table.objects.get(id=table_id)
    order_active=Table.objects.get(id=table_id).orders.all().filter(status='Active').first()
    categories = Category.objects.all()  # 获取所有分类及其酒水
    boissons=Boisson.objects.all()
    new_form=New_order_form()

    if request.method == 'POST':
        form =New_order_form(request.POST)
        if form.is_valid():
            
            adults=form.cleaned_data.get('adults')
            toddlers=form.cleaned_data.get('toddlers')
            kids=form.cleaned_data.get('kids')
            prix_boisson=0
                     
            if order_active:
                order_active.adults=adults
                order_active.kids=kids
                order_active.toddlers=toddlers
                order_active.save()
                boisson_ordered=Order_item.objects.filter(order=order_active).all()
                for b in boissons:
                    quantity=form.cleaned_data.get(f'boisson_{b.id}')
                    b.quantity=quantity
                    print(quantity)
                    if quantity:
                        b_old, created = boisson_ordered.get_or_create(boisson=b, defaults={'quantity': quantity},order=order_active)
                        b_old.quantity = quantity
                        b_old.save()
                        prix_boisson+=b.prix*int(quantity)
                        
                prix_person = Decimal(adults) * Decimal('15.8') + Decimal(kids) * Decimal('12.8') + Decimal(toddlers) * Decimal('9.8')
                prix_total = prix_person + prix_boisson
                order_active.prix=prix_total
                order_active.save()
                return render(request, 'restaurant/add_order_item.html', {
                    'adults': order_active.adults,
                    'kids': order_active.kids,
                    'toddlers': order_active.toddlers,
                    'boissons' : boissons,
                    'form':new_form,
                    'categories':categories,
                    'order':order_active
            })
            else:
                new_order=Order(adults=adults,kids=kids,toddlers=toddlers,table=table_this)
                new_order.save()

                for b in boissons:
                    quantity=form.cleaned_data.get(f'boisson_{b.id}')
                    b.quantity=quantity
                    if quantity:
                        new_order_item=Order_item(quantity=quantity,boisson=b,order=new_order)
                        prix_boisson+=b.prix*int(quantity)
                        new_order_item.save()
                # 使用固定的价格
                prix_person = Decimal(adults) * Decimal('15.8') + Decimal(kids) * Decimal('12.8') + Decimal(toddlers) * Decimal('9.8')
                prix_total = prix_person + prix_boisson
                new_order.prix=prix_total
                new_order.save()
                
                return render(request, 'restaurant/add_order_item.html', {
                    'adults': new_order.adults,
                    'kids': new_order.kids,
                    'toddlers': new_order.toddlers,
                    'boissons' : boissons,
                    'form':new_form,
                    'categories':categories,
                    'order':new_order
            })
    else:        
        if order_active:
            boisson_ordered=Order_item.objects.filter(order=order_active).all()
            for b in boissons:
                b.quantity = boisson_ordered.filter(boisson_id=b.id).values_list("quantity",flat=True).first() if boisson_ordered.filter(boisson_id=b.id).exists() else 0
            return render(request, 'restaurant/add_order_item.html', {
                    'adults': order_active.adults,
                    'kids': order_active.kids,
                    'toddlers': order_active.toddlers,
                    'boissons' : boissons,
                    'form':new_form,
                    'categories':categories,
                    'order':order_active
            })
        else:
            for b in boissons:
                b.quantity =0
            return render(request, 'restaurant/add_order_item.html', {
                    'adults': 0,
                    'kids': 0,
                    'toddlers': 0,
                    'boissons' : boissons,
                    'form':new_form,
                    'categories':categories,
                    'order':None
            })
    

@login_required(redirect_field_name="login")
def cashier_summary(request):
    # 获取所有活跃的订单，并按更新时间降序排列
    active_orders = Order.objects.filter(status='Active').prefetch_related('order_item_set__boisson').order_by('-updated_at')

    # 计算每个订单的总价和其他统计数据
    for order in active_orders:
        # 饮品总价
        boisson_total = sum(item.boisson.prix * item.quantity for item in order.order_item_set.all())
        # 人数价格
        prix_person = (Decimal(order.adults) * Decimal('15.8') +
                       Decimal(order.kids) * Decimal('12.8') +
                       Decimal(order.toddlers) * Decimal('9.8'))
        # 总价
        order.total_price = boisson_total + prix_person
    
    return render(request, 'restaurant/cashier_summary.html', {'orders': active_orders})



def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        print(user)
        if user is not None:
            login(request, user)
            return redirect('table_list')
        else:
            form = login_form()
            return render(request, 'restaurant/login.html', {'form': form})
    else:
        form = login_form()
        return render(request, 'restaurant/login.html', {'form': form})
    
    
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(redirect_field_name="login")
def clear_all_orders(request):
    if request.method == 'POST':
        # 获取所有订单
        orders = Order.objects.all()

        # 首先删除所有相关的订单项
        for order in orders:
            Order_item.objects.filter(order=order).delete()

        # 然后删除所有订单
        orders.delete()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})