from django.db import models


class CategoryItemsModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    image = models.URLField(blank=True, null=True, default=None)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)


class ShopItemsModel(models.Model):
    name = models.CharField(max_length=100)
    vendor_code = models.CharField(max_length=50, null=True)
    description = models.TextField(blank=True, null=True, default=None)
    price = models.FloatField(blank=True, default=0)
    discount_perc = models.IntegerField(blank=True, default=0)
    is_new = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    category = models.ForeignKey(CategoryItemsModel, null=True, related_name='items', on_delete=models.SET_NULL)
    colors = models.ForeignKey('self', blank=True, null=True, related_name='variable', on_delete=models.SET_NULL)


class ItemPictureModel(models.Model):
    url = models.URLField()
    item = models.ForeignKey(ShopItemsModel, related_name='item_pictures', on_delete=models.CASCADE)
