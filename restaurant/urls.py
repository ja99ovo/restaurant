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
    path('order_detail/', views.order_detail, name='order_detail'),
]
