from django import forms

from .models.client_event_history import ClientEventHistory
from .models.previous_list import PreviousList
from .models.previous_list_client import PreviousListClient
from .models.action import Action
from .models.lid import Lid
from .models.event import Event
from .models.event_plan import EventPlan
from .models.client import Client, State


class ClientEventHistoryForm(forms.ModelForm):

    class Meta:
        model = ClientEventHistory
        fields = ('client_id', 'event_plan_id', 'note',) 
        
class PreviousListForm(forms.ModelForm):
    event_id = forms.ModelChoiceField(queryset=Event.objects.all(), 
                                      label="Мероприятие без даты",
                                      required=False)
    event_plan_id = forms.ModelChoiceField(queryset=EventPlan.objects.filter(season="2023/2024"), 
                                           label="Мероприятие из расписания",
                                           required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = PreviousList
        fields = ('name', 'event_plan_id', 'event_id', 'description')
        
        
class LidForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = Lid
        fields = '__all__'
        
        
        
class ActionForm(forms.ModelForm):
    
    class Meta:
        model = Action
        fields = ('description', 'action', 
                  'note', 'stage', 'lid', 'state', 
                  'plc')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action'].widget.attrs.update({'class': 'form-control'})
        self.fields['stage'].widget.attrs.update({'class': 'form-control'})
        self.fields['lid'].widget.attrs.update({'class': 'form-control'})
        self.fields['plc'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['note'].widget.attrs.update({'class': 'form-control'})
        self.fields['state'].widget.attrs.update({'class': 'form-control'})


class AddClientsForm(forms.Form):
    clients = forms.CharField(max_length=5000)
    

class AddClientsSetForm(forms.Form):
    CHOICES_SOURCE= (
        ('irk', 'Иркутск'),
        ('angsk', 'Ангарск'),
        ('ykt', 'Якутск'),
        ('online', 'Онлайн'),
    )
    CHOICES_FILTER= (
        (None, 'Без фильтра'),
        ('no_base_course', 'Не курсовые'),
        ('is_base_course', 'Курсовые'),
        ('is_assisting', 'Ассистировали'),
        ('future_assisting', 'Хотят ассистировать'),
        ('is_school_level_1', 'Выпускники ИШ 1 ступени'),
        ('is_school_level_2', 'Выпускники ИШ 2 ступени'),
        ('ter_gr', 'Выпускники терапевтической группы'),
    )
    db = forms.MultipleChoiceField(label='База-источник', 
                                   choices=CHOICES_SOURCE)
    filter = forms.CharField(label='Фильтр', 
                             widget=forms.Select(choices=CHOICES_FILTER), 
                             required=False)
    state = forms.ModelMultipleChoiceField(label='Статус клиентов',
                                           queryset=State.objects.all())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})