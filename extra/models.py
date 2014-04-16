from django.db import models
from django.core.urlresolvers import reverse

class TextBit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    content = models.TextField()

    def get_update_url(self):
        return reverse('textbits:update', args=[self.pk])

    def __unicode__(self):
        return self.name
