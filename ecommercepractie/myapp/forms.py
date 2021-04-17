from django import forms
from myapp.models import Order,Customer
from django.contrib.auth.models import User



class CheckoutForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=("order_by","shipping_address","mobile","email")
