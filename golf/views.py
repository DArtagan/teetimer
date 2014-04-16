from django.views.generic import TemplateView
from guardian.mixins import LoginRequiredMixin
from datetime import date

from tracker.models import TeeTime
from extra.models import TextBit

class Index(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['object_list'] = TeeTime.objects.all() 
        context['textbit'] = TextBit.objects.get(name='Updates')
        today = date.today()
        context['month'] = "{0} {1}".format(today.year, today.month)
        if today.month == 12:
            context['month_next'] = "{0} {1}".format(today.year + 1, 1)
        else:
            context['month_next'] = "{0} {1}".format(today.year, today.month + 1)
        return context
