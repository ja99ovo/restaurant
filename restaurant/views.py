from .models import tables, orders, OrderItem,Boisson,table_order
from django.shortcuts import render, redirect, get_object_or_404
from .forms import New_order_form
from django.http import JsonResponse
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

def add_table(request):
    if request.method == 'POST':
        # 在这里处理添加新桌子的逻辑
        new_table = tables()  # 假设 'tables' 是你的桌子模型
        new_table.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def table_detail(request, table_id):
    pass

def order_detail(request, order_id):
    # 假设 table_order 模型关联到了订单和桌子
    order = get_object_or_404(table_order, id=order_id)

    # 假设 OrderItem 包含了订单中的项目信息
    items = OrderItem.objects.filter(order=order)

    # 计算订单总额
    total = sum(item.boisson.prix * item.quantity for item in items)

    return render(request, 'restaurant/order_detail.html', {
        'order': order,
        'items': items,
        'total': total
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

def login_view(request):
    # 如果是POST请求，处理登录逻辑
    if request.method == 'POST':
        # 从request.POST中获取用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 这里添加用户验证逻辑
        # ...
        # 验证成功后重定向或返回响应
        # ...
    # 如果不是POST请求，显示登录页面
    else:
        return render(request, 'login.html')