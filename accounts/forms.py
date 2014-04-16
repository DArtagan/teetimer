from django import forms
from localflavor.us.forms import USPhoneNumberField

from accounts.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone']

