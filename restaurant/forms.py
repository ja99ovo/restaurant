from django import forms
from .models import Table, Order, Order_item, Boisson
from .models import Category, Boisson
from django.contrib.auth.forms import AuthenticationForm

class New_order_form(forms.Form):
    adults = forms.IntegerField(label='adults', initial=0, widget=forms.HiddenInput())
    kids = forms.IntegerField(label='kids', initial=0, widget=forms.HiddenInput())
    toddlers = forms.IntegerField(label='toddlers', initial=0, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.prefetch_related('boissons').all()
        for category in categories:
            for boisson in category.boissons.all():
                self.fields[f'boisson_{boisson.id}'] = forms.IntegerField(
                    label=f'{category.name} - {boisson.name}', 
                    initial=0,
                    widget=forms.HiddenInput(),
                    required=False
                )


class Change_order_form(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['adults', 'kids', 'toddlers']
        widgets = {
            'adults': forms.HiddenInput(),
            'kids': forms.HiddenInput(),
            'toddlers': forms.HiddenInput(),
        }


class login_form(AuthenticationForm):
    username= forms.CharField(label='username' ,widget=forms.TextInput(attrs={'class':'form-control','required':''}))
    password= forms.CharField(label='password' ,widget=forms.PasswordInput(attrs={'class':'form-control','required':''}))