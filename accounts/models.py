from django.db import models
from authtools.models import AbstractNamedUser
from localflavor.us.models import PhoneNumberField

class User(AbstractNamedUser):
    phone = PhoneNumberField()

    def username():
        return self.email

    class Meta:
        db_table = 'auth_user'
        permissions = (
            ('manager_promotions', 'Manage promotions'),
        )

    def __unicode__(self):
        return self.name
