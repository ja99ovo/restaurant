from django import forms
from .models import tables, orders, OrderItem,Boisson,table_order


class New_order_form(forms.Form):
    adults= forms.IntegerField(label='adults' , initial=0,widget=forms.HiddenInput())
    kids = forms.IntegerField(label='kids' , initial=0,widget=forms.HiddenInput())
    toddlers = forms.IntegerField(label='toddlers' , initial=0,widget=forms.HiddenInput()) 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for boisson in Boisson.objects.all():
            self.fields[f'boisson_{boisson.name}'] = forms.CharField(label=f'{boisson.name}' , initial=0,widget=forms.HiddenInput())
            
            
            
class Change_order_form(forms.Form):
    adults= forms.IntegerField(label='adults' , initial=0,widget=forms.HiddenInput())
    kids = forms.IntegerField(label='kids' , initial=0,widget=forms.HiddenInput())
    toddlers = forms.IntegerField(label='toddlers' , initial=0,widget=forms.HiddenInput()) 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for boisson in Boisson.objects.all():
            self.fields[f'boisson_{boisson.name}'] = forms.CharField(label=f'{boisson.name}' , initial=0,widget=forms.HiddenInput())