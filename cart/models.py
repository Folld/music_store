from django.db import models
from django.contrib.auth.models import User
from items.models import ShopItemsModel


class CartModel(models.Model):
    user = models.ForeignKey(User, related_name='user_carts', on_delete=models.CASCADE)
    item = models.ForeignKey(ShopItemsModel, related_name='cart_items', on_delete=models.CASCADE)
