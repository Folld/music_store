from django import forms
from orders.models import OrderModel


class OrderCreateForm(forms.ModelForm):
    delivery_price = forms.FloatField()
    delivery_type = forms.CharField()

    class Meta:
        model = OrderModel
        fields = ('delivery_price', 'delivery_type')
