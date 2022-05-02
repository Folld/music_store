from django.conf import settings
from django.db.models import F, Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.http import HttpResponse, HttpResponseRedirect

from cart.models import CartModel
from items.models import ShopItemsModel, CategoryItemsModel
from orders.models import OrderModel, OrderItemsModel
from web_ui.forms import OrderCreateForm


class ItemsView(ListView):
    template_name = 'items/items-list.html'
    template_engine = 'jinja2'
    context_object_name = 'items'
    model = ShopItemsModel

    def get_context_data(self, **kwargs):
        category = CategoryItemsModel.objects.get(id=self.kwargs.get('category'))
        kwargs.update({
            'pageview': category.parent.name if category.parent else category.name,
            'heading': category.name,
        })
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.model.objects.filter(category_id=self.kwargs.get('category'))


class ItemsDetailView(DetailView):
    template_name = 'items/items-detail.html'
    template_engine = 'jinja2'
    context_object_name = 'item'
    model = ShopItemsModel

    def get_context_data(self, **kwargs):
        kwargs.update({
            'pageview': self.object.category.parent.name if self.object.category.parent else self.object.category.name,
            'heading': self.object.category.name,
            'in_cart': CartModel.objects.filter(user_id=self.request.user.pk, item=self.object).exists()
        })
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        if not kwargs.get('pk'):
            return self.get(request, *args, **kwargs)
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user = self.request.user
        item = ShopItemsModel.objects.get(id=kwargs['pk'])
        create, cart = CartModel.objects.get_or_create(user=user, item=item)
        if create:
            return self.get(request, *args, **kwargs)
        return self.get(request, *args, **kwargs)


class HomePageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'pageview': 'Homepage',
            'heading': 'Home',
        })
        return super().get_context_data(**kwargs)


class OrdersView(ListView):
    template_name = 'orders/orders-list.html'
    model = OrderModel

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'pageview': 'Orders',
            'heading': 'Orders',
        })
        return super().get_context_data(**kwargs)


class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    model = OrderModel
    form_class = OrderCreateForm
    success_url = reverse_lazy('orders-list')

    def form_valid(self, form):
        form.clean()
        data = form.cleaned_data
        user = self.request.user
        carts = CartModel.objects.filter(user=user)
        ordered_items = ShopItemsModel.objects.filter(id__in=carts.values('item'))
        data.update({
            "price": sum(ordered_items.values_list('price', flat=True)),
            "user": user,
        })
        order = OrderModel(**data)
        order.save()
        order_items = []
        for item in ordered_items:
            order_items.append(OrderItemsModel(item=item, order=order))
        OrderItemsModel.objects.bulk_create(order_items)
        carts.delete()
        return HttpResponseRedirect(redirect_to=reverse_lazy('orders-list'))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'pageview': 'Order create',
            'heading': 'Order',
            'carts': CartModel.objects.filter(user=self.request.user),
            'delivery_types': self.model.DELIVERY_TYPES
        })
        return super().get_context_data(**kwargs)


class CartView(ListView):
    template_name = 'cart/cart.html'
    model = CartModel
    context_object_name = 'carts'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'pageview': 'Cart',
            'heading': 'Cart',
            'total_price': self.get_queryset().aggregate(total_price=Sum(F('item__price')))
        })
        return super().get_context_data(**kwargs)


def delete_cart(request, item_id):
    CartModel.objects.filter(item_id=item_id, user_id=request.user.pk).delete()
    return HttpResponseRedirect(reverse_lazy('cart-list'))

