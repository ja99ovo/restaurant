from django.urls import path
from . import views

from django.contrib import admin
urlpatterns = [
    path(r'^admin/', admin.site.urls),
    path('', views.table_list, name='table_list'),

    path('base/', views.base, name='base'),
    path('add_order_item/', views.add_order_item, name='add_order_item'),
    path('add_table/', views.add_table, name='add_table'),
    path('table/<int:table_id>/add_order_item/<int:order_id>/', views.add_order_item, name='add_order_item_with_order'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('clear_all_orders/', views.clear_all_orders, name='clear_all_orders'),
    path('cashier_summary/', views.cashier_summary, name='cashier_summary'),
]
