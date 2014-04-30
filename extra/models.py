from django.db import models
from django.core.urlresolvers import reverse

class TextBit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    content = models.TextField()

    def get_update_url(self):
        return reverse('textbits:update', args=[self.pk])

    def __unicode__(self):
        return self.name

class Title(models.Model):
    field = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

    def __unicode__(self):
        return self.name
