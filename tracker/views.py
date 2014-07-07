from django.shortcuts import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse
from guardian.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime, time, date
from calendar import month_name

from tracker.models import TeeTime
from tracker.forms import *

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

class Times(TeeTimeMixin, LoginRequiredMixin, ListView):
    template_name = 'tracker/times.html'

    def get_context_data(self, **kwargs):
        context = super(TeeTimeMixin, self).get_context_data(**kwargs)
        context['object_list'] = context['object_list'].filter(time__year=datetime.now().year)
        return context

class Detail(TeeTimeMixin, LoginRequiredMixin, DetailView):
    template_name = 'tracker/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TeeTimeMixin, self).get_context_data(**kwargs)
        print(context['object'].Slot)
        return context

class Date(TeeTimeMixin, LoginRequiredMixin, ListView):
    template_name = 'tracker/date.html'

    def dispatch(self, request, *args, **kwargs):
        self.year, self.month, self.day = self.kwargs['date'].split('-')
        return super(Date, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeeTimeMixin, self).get_context_data(**kwargs)
        context['teetime_list'].filter(time__year=self.year, time__month=self.month, time__day=self.day)
        context['month'] = "{0} {1}".format(self.year, self.month)
        raw_list = context['object_list']
        context['object_list'] = {}
        for slot in raw_list:
            if slot.time not in context['object_list']:
                context['object_list'][slot.time] = []
            temp = context['object_list'][slot.time]
            temp.append(slot)
            context['object_list'][slot.time] = temp
        context['object_list'] = sorted(context['object_list'].items())
        if self.month == '12':
            context['month_next'] = "{0} {1}".format(int(self.year) + 1, 1)
        else:
            context['month_next'] = "{0} {1}".format(self.year, int(self.month) + 1)
        context['datetimes'] = TeeTime.objects.all()
        context['title'] = "{0} {1}, {2}".format(month_name[int(self.month)], self.day, self.year)
        return context

    def get_queryset(self):
        return TeeTime.objects.filter(time__range=(datetime.combine(datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date(), time.min), datetime.combine(datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date(), time.max)))


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

class Create(TeeTimeMixin, LoginRequiredMixin, FormView):
    template_name = 'tracker/create.html'
    form_class = CreateForm

    def form_valid(self, form):
        self.teetime_time = form.instance.time
        form.instance.pk = None
        repeat = form.save(commit=False)
        for i in range(0,int(form.data['slots'])):
            repeat.pk = None
            repeat.save()
        return super(Create, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('tracker:day', kwargs={'date': (self.teetime_time).strftime('%Y-%m-%d')})

class Update(TeeTimeMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tracker/update.html'

class Delete(TeeTimeMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tracker/delete.html'

@login_required
def claim(request, pk):
    teetime = TeeTime.objects.get(pk=pk)
    teetime.person = request.user
    teetime.save()
    return HttpResponseRedirect(reverse('tracker:day', kwargs={'date': (teetime.time).strftime('%Y-%m-%d')}))

@login_required
def unclaim(request, pk):
    teetime = TeeTime.objects.get(pk=pk)
    teetime.person = None
    teetime.save()
    return HttpResponseRedirect(reverse('tracker:day', kwargs={'date': (teetime.time).strftime('%Y-%m-%d')}))
