from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from guardian.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from authtools.forms import UserCreationForm
from guardian.models import Group

from accounts.models import User
from accounts.forms import EmailForm

class AddUser(LoginRequiredMixin, FormView):
    form_class = UserCreationForm
    model = User
    template_name = 'accounts/add_user.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(AddUser, self).form_valid(form)

class Admins(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'

class EmailUpdate(LoginRequiredMixin, FormView):
    template_name = 'accounts/update_email.html'
    form_class = EmailForm
    model = User
    success_url = '/'

    def form_valid(self, form):
        self.request.user.email = form.cleaned_data.get('email')
        self.request.user.save(update_fields=['email'])
        return super(EmailUpdate, self).form_valid(form)

@login_required
def promote(request, pk):
    user = User.objects.get(pk=pk)
    g = Group.objects.get(name='manager')
    g.user_set.add(user)
    return HttpResponseRedirect(reverse('accounts:admin_users'))

@login_required
def demote(request, pk):
    user = User.objects.get(pk=pk)
    g = Group.objects.get(name='manager')
    g.user_set.remove(user)
    return HttpResponseRedirect(reverse('accounts:admin_users'))
