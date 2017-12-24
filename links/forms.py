from django.forms import ModelForm
from links.models import Interval
from django import forms


class IntervalForm(ModelForm):
    class Meta:
        model = Interval
        fields = ['value']
        labels = {'value': 'Interval', }
        widgets = {
            'value': forms.TextInput(
                attrs={'placeholder': 'Set interval in seconds'}),
        }
