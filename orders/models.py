from cart.models import CartModel
from django.db import models
from items.models import ShopItemsModel


class OrderModel(models.Model):
    DELIVERY_TYPES = (
        ('0', 'pickup'),
        ('1', 'delivery'),
    )
    total_price = models.FloatField()
    address = models.CharField(max_length=255)
    delivery_type = models.CharField(choices=DELIVERY_TYPES, max_length=4)


class OrderItemsModel(models.Model):
    item_id = models.ForeignKey(ShopItemsModel, related_name='order_items', on_delete=models.CASCADE)
    order = models.ForeignKey(OrderModel, related_name='order_items', on_delete=models.CASCADE)
    delivery_price = models.FloatField(default=0)
