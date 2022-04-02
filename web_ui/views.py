from django.views.generic import ListView, TemplateView, DetailView

from web_ui.models import ShopItemsModel, CategoryItemsModel


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
