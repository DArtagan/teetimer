from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from guardian.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from authtools.forms import UserCreationForm
from guardian.models import Group

from accounts.models import User
from accounts.forms import ProfileForm

class AddUser(LoginRequiredMixin, FormView):
    form_class = UserCreationForm
    model = User
    template_name = 'accounts/add_user.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(AddUser, self).form_valid(form)

class Members(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'

    def get_queryset(self):
        return User.objects.all().order_by('name')

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/update_profile.html'
    form_class = ProfileForm
    model = User
    success_url = '/'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

@login_required
def promote(request, pk):
    user = User.objects.get(pk=pk)
    g = Group.objects.get(name='manager')
    g.user_set.add(user)
    return HttpResponseRedirect(reverse('accounts:members'))

@login_required
def demote(request, pk):
    user = User.objects.get(pk=pk)
    g = Group.objects.get(name='manager')
    g.user_set.remove(user)
    return HttpResponseRedirect(reverse('accounts:members'))
