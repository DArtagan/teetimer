from django.views.generic.edit import UpdateView
from guardian.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse

from extra.models import TextBit

class Update(LoginRequiredMixin, UpdateView):
    model = TextBit
    template_name = 'extra/update.html'
    def get_success_url(self):
        return reverse('index')
