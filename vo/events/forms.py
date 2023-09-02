from django import forms

from .models.event import Event
from .models.event_plan import EventPlan

class EventForm(forms.ModelForm):
    
    sort_choices = [
        ('inner', 'Наше'),
        ('top', 'ТОП'),
        ('session', 'Сессия, экзамен и т.д.'),
        ('seminar', 'Семинар (Хакоми, Травмы и тд)'),
    ]

    sort = forms.ChoiceField(choices=sort_choices, initial='inner')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'rows': 2})
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Event
        fields = '__all__'
        
        
class EventPlanForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'дд.мм.гггг'}, format='%d.%m.%Y')
    )
    end_date = forms.DateTimeField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'дд.мм.гггг'}, format='%d.%m.%Y')
    )
    
    start_time = forms.DateTimeField(
        input_formats=['%H:%M'],
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM'}, format='%H:%M')
    )
    end_time = forms.DateTimeField(
        input_formats=['%H:%M'],
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM'}, format='%H:%M')
    )

    class Meta:
        model = EventPlan
        fields = ('season', 'event', 'place', 'is_period', 'site', 'period','user')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

