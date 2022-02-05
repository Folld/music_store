from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'partition/starterpage.html'
    template_engine = 'jinja2'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'pageview': 'index',
            'heading': 'head',
        })
        return super().get_context_data(**kwargs)
