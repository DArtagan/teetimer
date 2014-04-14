from django.shortcuts import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from guardian.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime, time, date

from tracker.models import TeeTime

class TeeTimeMixin(object):
    model = TeeTime
    def get_success_url(self):
        return reverse('tracker:detail', kwargs={'pk': self.object.pk})

class Index(TeeTimeMixin, LoginRequiredMixin, ListView):
    template_name = 'tracker/index.html'

class Detail(TeeTimeMixin, LoginRequiredMixin, DetailView):
    template_name = 'tracker/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TeeTimeMixin, self).get_context_data(**kwargs)
        count = context['object'].slots - context['object'].people.count()
        context['openings'] = range(0, count)
        return context

class Date(TeeTimeMixin, LoginRequiredMixin, ListView):
    template_name = 'tracker/date.html'

    def get_queryset(self):
        print(self.kwargs['date'])
        return TeeTime.objects.filter(time__range=(datetime.combine(datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date(), time.min), datetime.combine(datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date(), time.max)))

    def get_context_data(self, **kwargs):
        context = super(TeeTimeMixin, self).get_context_data(**kwargs)
        for instance in context['object_list']:
            count = instance.slots - instance.people.count()
            instance.openings = range(0, count)
        return context


class Create(TeeTimeMixin, LoginRequiredMixin, CreateView):
    template_name = 'tracker/create.html'

class Update(TeeTimeMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tracker/update.html'

class Delete(TeeTimeMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tracker/delete.html'
    def get_success_url(self):
        return reverse('index')

@login_required
def claim(request, pk):
    teetime = TeeTime.objects.get(pk=pk)
    if teetime.slots > teetime.people.count():
        teetime.people.add(request.user)
    return HttpResponseRedirect(reverse('tracker:date', kwargs={'date': (teetime.time).strftime('%Y-%m-%d')}))
