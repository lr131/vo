from django import forms
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


from .models.client_event_history import ClientEventHistory
from .models.previous_list import PreviousList
from .models.previous_list_client import PreviousListClient
from .models.action import Action
from .models.lid import Lid
from .models.event import Event
from .models.event_plan import EventPlan
from .models.client import Client, State


class EventPlanChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.event.event_type.name} {obj.event.name} - {obj.start_date:%d.%m.%Y} ({obj.place})'


class ClientEventHistoryForm(forms.ModelForm):

    class Meta:
        model = ClientEventHistory
        fields = ('client_id', 'event_plan_id', 'note',) 
        
class PreviousListForm(forms.ModelForm):
    
    
    down_date = timezone.now() - timedelta(days=1) # end_date__gte
    update = timezone.now() + timedelta(days=365) # start_date__lte
    
    qs = EventPlan.objects.filter(
        end_date__gte=down_date,
        start_date__lte=update,
        is_period=False
    )
    
    event_id = forms.ModelChoiceField(queryset=Event.objects.all().order_by('name'), 
                                      label="Мероприятие без даты",
                                      required=False)
    event_plan_id = EventPlanChoiceField(queryset=qs.order_by('start_date'), 
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
    
    down_date = timezone.now() - timedelta(days=1) # end_date__gte
    update = timezone.now() + timedelta(weeks=15) # start_date__lte
    
    qs = EventPlan.objects.filter(
        end_date__gte=down_date,
        start_date__lte=update,
        season="2023/2024",
        is_period=False
    )
    
    event_id = EventPlanChoiceField(queryset=qs.order_by('start_date'), 
                                           label="Выберите мероприятие",
                                           required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = Lid
        exclude = ['event_id']  # Исключаем поле 'event_id'
        
        
        
        
class ActionForm(forms.ModelForm):
    
    class Meta:
        model = Action
        fields = ('description', 'action', 
                  'note', 'stage', 'lid', 'state', 
                  'plc')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action'].widget.attrs.update({'class': 'form-control', 'placeholder': "Рассылка, звонок, смс"})
        self.fields['stage'].widget.attrs.update({'class': 'form-control', 'placeholder': "Приглашение, работа с возражениями и т.д."})
        self.fields['lid'].widget.attrs.update({'class': 'form-control'})
        self.fields['plc'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 3, 'placeholder': "Коротко о течении разговора, важные ключевые, на ваш взгляд, моменты, которые нужно знать перед следующим контактом"})
        self.fields['note'].widget.attrs.update({'class': 'form-control', 'rows': 3, 'placeholder': "К чему пришли в диалоге. Если контакт не состоялся, то так и пишем"})
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