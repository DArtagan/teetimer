from django import forms
from tracker.models import TeeTime

class CreateForm(forms.ModelForm):
    #number = forms.IntegerField()
    class Meta:
        model = TeeTime
        fields = ['time', 'person']
