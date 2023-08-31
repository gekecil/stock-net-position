from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.urls import reverse, resolve
from ..models import NavLink

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'contents/dashboard.html'

    def get_context_data(self, **kwargs):
        chart_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des']
        #now = datetime.datetime.now()

        #line_chart = {
        #    'datasets': [
        #        {'model': User.objects, 'label': 'Users', 'data': {}},
        #        {'model': UserPosition.objects, 'label': 'Positions', 'data': {}},
        #        {'model': UserSegmentation.objects, 'label': 'Segmentations', 'data': {}},
        #    ]
        #}

        #for key, label in enumerate(chart_labels[0:now.month]):
        #    for dataset in line_chart['datasets']:
        #        model = dataset['model'].filter(pub_date__date__lt=datetime.date(now.year, key+1, 1))
        #        dataset['data'][label] = model.count()

        #        if key == len(chart_labels[0:now.month]) - 1:
        #            dataset.pop('model')

        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = NavLink.objects.get(path=self.request.path).title
        context['nav_links'] = NavLink.objects.order_by('pub_date').all()
        #context['line_chart'] = line_chart

        return context
