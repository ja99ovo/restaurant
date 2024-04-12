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
def order_detail(request, table_id):  # 添加 table_id 参数
    # 使用 table_id 从数据库中获取对应的 Table 对象
    table = get_object_or_404(Table, id=table_id)
    order = table.orders.filter(status='Active').first()

    boissons_sa = Boisson.objects.filter(category__name='COCKTAILS SA')
    boissons_aa = Boisson.objects.filter(category__name='COCKTAILS AA')

    # 创建或获取一个 form 实例，这里假设 form 已经定义
    form = Change_order_form(instance=order if order else None)

    if request.method == 'POST':
        form = Change_order_form(request.POST)
        if form.is_valid():
            adults = form.cleaned_data.get('adults')
            kids = form.cleaned_data.get('kids')
            toddlers = form.cleaned_data.get('toddlers')
            if order:  # Ensure the order exists
                order.adults = adults
                order.kids = kids
                order.toddlers = toddlers
                order.save()

                # Reset prix_boisson for this calculation
                prix_boisson = 0

                for boisson in Boisson.objects.all():
                    quantity = form.cleaned_data.get(f'boisson_{boisson.id}')
                    order_item, created = Order_item.objects.get_or_create(order=order, boisson=boisson)
                    if quantity is not None:
                        order_item.quantity = int(quantity)
                        order_item.save()
                        prix_boisson += boisson.prix * int(quantity)

                # Calculate the total price using fixed values
                prix_person = adults * 15.8 + kids * 12.8 + toddlers * 9.8
                prix_total = prix_person + prix_boisson
                order.prix = prix_total
                order.save()
                # After saving, redirect to prevent form resubmission
                return redirect('order_detail', table_id=table.id)
        else:
            print(form.errors)
    else:
        form = Change_order_form(initial={'adults': order.adults if order else 0,
                                          'kids': order.kids if order else 0,
                                          'toddlers': order.toddlers if order else 0})

    # Include existing order item quantities in the context
    boisson_quantities = {}
    if order:
        boisson_ordered = Order_item.objects.filter(order=order)
        for item in boisson_ordered:
            boisson_quantities[item.boisson.id] = item.quantity

    context = {
        'table': table,
        'order': order,
        'form': form,
        'boissons_sa': boissons_sa,
        'boissons_aa': boissons_aa,
        'boisson_quantities': boisson_quantities,
    }
    return render(request, 'restaurant/order_detail.html', context)


def cashier_summary(request):
    pass

@login_required(redirect_field_name="login")
def add_order_item(request):
    table_id = request.GET.get('table_id')
    table_this = get_object_or_404(Table, id=table_id)

    if request.method == 'POST':
        form = New_order_form(request.POST)
        
        if form.is_valid():
            adults = form.cleaned_data.get('adults')
            kids = form.cleaned_data.get('kids')
            toddlers = form.cleaned_data.get('toddlers')
            
            new_order = Order(adults=adults, kids=kids, toddlers=toddlers, table=table_this)
            new_order.save()

            prix_boisson = 0

            for category in Category.objects.all():
                boissons = Boisson.objects.filter(category=category)
                
                for boisson in boissons:
                    boisson_key = f'boisson_{boisson.id}'
                    quantity = form.cleaned_data.get(boisson_key, 0)

                    if quantity:
                        Order_item.objects.create(order=new_order, boisson=boisson, quantity=quantity)
                        prix_boisson += boisson.prix * quantity
            
            # 使用固定的价格
            prix_person = adults * 15.8 + kids * 12.8 + toddlers * 9.8
            prix_total = prix_person + prix_boisson
            
            new_order.prix = prix_total
            new_order.save()

            return redirect('order_detail', table_id=table_this.id)
        else:
            # 打印错误信息到控制台
            print(form.errors)
    
    else:
        form = New_order_form()

    # 传递SA和AA分类的酒水到模板
    context = {
        'form': form,
        'table': table_this,
        'boissons_sa': Boisson.objects.filter(category__name='COCKTAILS SA'),
        'boissons_aa': Boisson.objects.filter(category__name='COCKTAILS AA')
    }
    
    return render(request, 'restaurant/add_order_item.html', context)

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