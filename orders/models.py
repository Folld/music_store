from django.contrib.auth.models import User
from django.db import models


class OrderModel(models.Model):
    DELIVERY_TYPES = (
        ('0', 'pickup'),
        ('1', 'delivery'),
    )
    price = models.FloatField()
    address = models.CharField(max_length=255)
    delivery_type = models.CharField(choices=DELIVERY_TYPES, max_length=4)
    user = models.ForeignKey(User, related_name='user_orders', on_delete=models.CASCADE)


class OrderItemsModel(models.Model):
    item_id = models.IntegerField()
    order = models.ForeignKey(OrderModel, related_name='order_items', on_delete=models.CASCADE)
    delivery_price = models.FloatField(default=0)
