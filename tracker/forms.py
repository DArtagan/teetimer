from django import forms
from tracker.models import TeeTime

class CreateForm(forms.ModelForm):
    number = forms.IntegerField(initial=4)
    class Meta:
        model = TeeTime
        fields = ['time', 'number', 'person']
