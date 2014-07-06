from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

class TeeTime(models.Model):
    time = models.DateTimeField()
    person = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    date_edited = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return reverse('tracker:detail', args=[self.pk])

    def get_update_url(self):
        return reverse('tracker:update', args=[self.pk])

    def get_delete_url(self):
        return reverse('tracker:delete', args=[self.pk])

    def get_claim_url(self):
        return reverse('tracker:claim', args=[self.pk])

    def get_unclaim_url(self):
        return reverse('tracker:unclaim', args=[self.pk])

    def get_date_url(self):
        return reverse('tracker:day', args=[(teetime.time).strftime('%Y-%m-%d')])

    def __unicode__(self):
        return self.time.strftime('%Y-%m-%d')

