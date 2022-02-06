from django.views.generic import ListView, TemplateView

from web_ui.models import ShopItemsModel


class ElectricGuitarsView(ListView):
    template_name = 'items/items-list.html'
    template_engine = 'jinja2'
    context_object_name = 'items'
    model = ShopItemsModel

    def get_context_data(self, **kwargs):
        kwargs.update({
            'pageview': 'Electric items',
            'heading': 'Guitars',
        })
        return super().get_context_data(**kwargs)


class HomePageView(TemplateView):
    template_name = 'partition/starterpage.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'pageview': 'Homepage',
            'heading': 'Home',
        })
        return super().get_context_data(**kwargs)
