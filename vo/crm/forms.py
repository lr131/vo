from django import forms

from .models import ClientEventHistory

class ClientEventHistoryForm(forms.ModelForm):

    class Meta:
        model = ClientEventHistory
        fields = ('client_id', 'event_plan_id', 'note',) 