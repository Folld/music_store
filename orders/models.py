from django.contrib.auth.models import User
from cart.models import CartModel
from django.db import models
from items.models import ShopItemsModel


class OrderModel(models.Model):
    DELIVERY_TYPES = (
        ('0', 'pickup'),
        ('1', 'delivery'),
    )
    price = models.FloatField()
    delivery_price = models.FloatField(default=0)
    address = models.CharField(max_length=255)
    delivery_type = models.CharField(choices=DELIVERY_TYPES, max_length=4)
    user = models.ForeignKey(User, related_name='user_orders', on_delete=models.CASCADE)


class OrderItemsModel(models.Model):
    item = models.ForeignKey(ShopItemsModel, related_name='order_items', on_delete=models.CASCADE)
    order = models.ForeignKey(OrderModel, related_name='order_items', on_delete=models.CASCADE)
