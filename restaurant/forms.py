from django import forms
from .models import tables, orders, OrderItem,Boisson,table_order


class New_order(forms.Form):
    adult= forms.IntegerField()
    kids = forms.IntegerField()
    toddlers = forms.IntegerField()
    for b in Boisson.objects.all():
        b=forms.IntegerField()