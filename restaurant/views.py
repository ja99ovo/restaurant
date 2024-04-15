from .models import Table, Order, Order_item,Boisson, Category
from django.shortcuts import render, redirect, get_object_or_404
from .forms import New_order_form, Change_order_form,login_form
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

@login_required(redirect_field_name="login_view")
def order_detail(request):
    table_id = request.GET.get('table_id')
    boissons=Boisson.objects.all()
    
    order_obj=Table.objects.get(id=table_id).orders.all().filter(status='Active').first()
    boisson_ordered=Order_item.objects.filter(order_id=order_obj.id).all()
    
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
            prix_boisson=0
            quantity=form.cleaned_data.get(f'boisson_{b.name}')
            if quantity:
                b_old=boisson_ordered.filter(boisson=b).all().first()
                prix_boisson+=b.prix*int(quantity)
                b_old.quantity=quantity
                b_old.save()
        prix_person=adults*3+kids*2+toddlers
        prix_total=prix_boisson+prix_person
        order_obj.prix=prix_total
        order_obj.save()
    form = Change_order_form()
    for b in boissons:
        
        b.quantity = boisson_ordered.filter(boisson_id=b.id).values_list("quantity",flat=True).first() if boisson_ordered.filter(boisson_id=b.id).exists() else 0
    return render(request, 'restaurant/order_detail.html', {
        'adults':order_obj.adults,
        'kids':order_obj.kids,
        'toddlers':order_obj.toddlers,
        'form':form,
        'boissons': boissons,
        'order':order_obj,
    })


def cashier_summary(request):
    pass

@login_required(redirect_field_name="login")
def add_order_item(request):
    categories = Category.objects.prefetch_related('boissons').all()  # 获取所有分类及其酒水
    table_id = request.GET.get('table_id')
    table_this=Table.objects.get(id=table_id)
    if request.method == 'POST':
        form =New_order_form(request.POST)
        
        if form.is_valid():
            adults=form.cleaned_data.get('adults')
            toddlers=form.cleaned_data.get('toddlers')
            kids=form.cleaned_data.get('kids')
            
            new_order=Order(adults=adults,kids=kids,toddlers=toddlers,table=table_this)
            new_order.save()

            prix_boisson=0
            for b in boissons:
                quantity=form.cleaned_data.get(f'boisson_{b.name}')
                if quantity:
                    new_order_item=Order_item(quantity=quantity,boisson=b,order=new_order)
                    prix_boisson+=b.prix*int(quantity)
                    new_order_item.save()
            # 使用固定的价格
            prix_person = Decimal(adults) * Decimal('15.8') + Decimal(kids) * Decimal('12.8') + Decimal(toddlers) * Decimal('9.8')
            prix_total = prix_person + prix_boisson
            new_order.prix=prix_total
            new_order.save()
            #重定向到订单修改页面
            new_form=Change_order_form()
            boisson_ordered=Order_item.objects.filter(order=new_order).all()
            for b in boissons:
                b.quantity = boisson_ordered.filter(boisson_id=b.id).values_list("quantity",flat=True).first() if boisson_ordered.filter(boisson_id=b.id).exists() else 0
            return render(request, 'restaurant/order_detail.html', {
                'form': Change_order_form(instance=new_order),
                'categories': categories,  # 将分类传递到模板
                'order': new_order
            })
        else:
            form = New_order_form()
    else:
        form = New_order_form()
    return render(request, 'restaurant/add_order_item.html', {
        'form': form,
        'categories': categories  # 将分类传递到模板
    })


def cashier_summary(request):
    pass

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