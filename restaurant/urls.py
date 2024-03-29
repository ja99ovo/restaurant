from django.urls import path
from . import views

urlpatterns = [
    path('', views.table_list, name='table_list'),
    path('login/', views.login_view, name='login'),
    path('add_order_item/', views.add_order_item, name='add_order_item'),
    path('add_table/', views.add_table, name='add_table'),
    path('table/<int:table_id>/add_order_item/<int:order_id>/', views.add_order_item, name='add_order_item_with_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cashier/', views.cashier_summary, name='cashier_summary'),
    path('clear_orders/', views.clear_orders, name='clear_orders'),
    path('order/clear/<int:order_id>/', views.clear_order, name='clear_order'),
]
