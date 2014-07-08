from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from tracker.models import TeeTime

class CreateForm(forms.ModelForm):
    slots = forms.IntegerField(initial=4)
    class Meta:
        model = TeeTime
        fields = ['time', 'slots', 'person']
        widgets = {
            'time': DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                            "useSeconds": False,
                                            "minuteStepping": 5,
                                            "sideBySide": True,}),
        }
