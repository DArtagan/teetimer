from django.shortcuts import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from guardian.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime, time, date
from calendar import month_name

from tracker.models import TeeTime

class TeeTimeMixin(object):
    model = TeeTime
    def get_success_url(self):
        return reverse('tracker:day', kwargs={'date': (self.object.time).strftime('%Y-%m-%d')})

class Index(TeeTimeMixin, LoginRequiredMixin, ListView):
    template_name = 'tracker/index.html'

    def get_context_data(self, **kwargs):
        context = super(TeeTimeMixin, self).get_context_data(**kwargs)
        today = date.today()
        context['month'] = "{0} {1}".format(today.year, today.month)
        if today.month == 12:
            context['month_next'] = "{0} {1}".format(today.year + 1, 1)
        else:
            context['month_next'] = "{0} {1}".format(today.year, today.month + 1)
        return context

class Detail(TeeTimeMixin, LoginRequiredMixin, DetailView):
    template_name = 'tracker/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TeeTimeMixin, self).get_context_data(**kwargs)
        count = context['object'].slots - context['object'].people.count()
        context['openings'] = range(0, count)
        return context

class Date(TeeTimeMixin, LoginRequiredMixin, ListView):
    template_name = 'tracker/date.html'

    def dispatch(self, request, *args, **kwargs):
        self.year, self.month, self.day = self.kwargs['date'].split('-')
        return super(Date, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(TeeTimeMixin, self).get_context_data(**kwargs)
        for instance in context['object_list']:
            count = instance.slots - instance.people.count()
            instance.openings = range(0, count)
        context['month'] = "{0} {1}".format(self.year, self.month)
        if self.month == '12':
            context['month_next'] = "{0} {1}".format(int(self.year) + 1, 1)
        else:
            context['month_next'] = "{0} {1}".format(self.year, int(self.month) + 1)
        context['title'] = "{0} {1}, {2}".format(month_name[int(self.month)], self.day, self.year)
        return context

class Month(TeeTimeMixin, LoginRequiredMixin, ListView):
    template_name = 'tracker/month.html'

    def dispatch(self, request, *args, **kwargs):
        self.year, self.month = self.kwargs['date'].split('-')
        return super(Month, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeeTimeMixin, self).get_context_data(**kwargs)
        context['month'] = "{0} {1}".format(self.year, self.month)
        if self.month == '12':
            context['month_next'] = "{0} {1}".format(int(self.year) + 1, 1)
        else:
            context['month_next'] = "{0} {1}".format(self.year, int(self.month) + 1)
        return context
        context['title'] = "{0} {1}".format(month_name[int(self.month)], self.year)
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
    return HttpResponseRedirect(reverse('tracker:day', kwargs={'date': (teetime.time).strftime('%Y-%m-%d')}))
