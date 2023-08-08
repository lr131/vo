from django import forms

from .models.event import Event
from .models.event_plan import EventPlan

class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Event
        fields = '__all__'
        
        
class EventPlanForm(forms.ModelForm):

    class Meta:
        model = EventPlan
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

