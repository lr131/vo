from django import forms

from .models import ClientEventHistory, PreviousList, Action

class ClientEventHistoryForm(forms.ModelForm):

    class Meta:
        model = ClientEventHistory
        fields = ('client_id', 'event_plan_id', 'note',) 
        
class PreviousListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = PreviousList
        fields = ('name', 'description',)
        
        
        
class ActionForm(forms.ModelForm):
    
    class Meta:
        model = Action
        fields = ('description', 'action', 
                  'note', 'stage', 'lid', 
                  'plc')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action'].widget.attrs.update({'class': 'form-control'})
        self.fields['stage'].widget.attrs.update({'class': 'form-control'})
        self.fields['lid'].widget.attrs.update({'class': 'form-control'})
        self.fields['plc'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['note'].widget.attrs.update({'class': 'form-control'})
        # self.fields['worker'].widget.attrs.update({'class': 'form-control'})