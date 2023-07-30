from dataclasses import field
from email.policy import default
from django import forms

from .models import Mailing, MailingDetail, State, SocialPlace, Links
from .const import MAILING_SOURCE_TYPES, MAILING_RESULT_CHOISES, SOURCE_MAILING_STATE


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ('name', 'description', 'source_type')
        
        
class MailingDetailForm(forms.ModelForm):
    class Meta:
        model = MailingDetail
        fields = '__all__'
        

class SocialPlaceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = SocialPlace
        fields = '__all__'
        

class LinksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Links
        fields = '__all__'

class LinkSpeedForm(forms.Form):
    name = forms.CharField(label='Наименование (что за ссылка)', 
                           max_length=500, required=True)
    link = forms.CharField(label='ссылка (без меток)', 
                           max_length=500, required=True)
    source = forms.CharField(label='Для чего ссылка', 
                             widget=forms.Select(choices=MAILING_SOURCE_TYPES))
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class MailindQuickDetailForm(forms.Form):
    CHOICES_MSGRS = (
        ('wa', 'WhatsApp'),
        ('viber', 'Viber'),
        ('tg', 'Telegram'),
        ('sms', 'Смс'),
    )
    id = forms.IntegerField()
    state = forms.CharField(label='Статус работы', 
                             widget=forms.Select(choices=MAILING_RESULT_CHOISES))
    source = forms.CharField(label='Месседжер', 
                             widget=forms.Select(choices=CHOICES_MSGRS))
    
class UploadWapicoReportForm(forms.Form):
    file = forms.FileField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'custom-file-input'})

class MailindBDForm(forms.Form):
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
    db = forms.CharField(label='База-источник', widget=forms.Select(choices=CHOICES_SOURCE))
    filter = forms.CharField(label='фильтр (курсовые/не курсовые)', 
                             widget=forms.Select(choices=CHOICES_FILTER), 
                             required=False)
    msg = forms.CharField(label='текст (шаблон)', widget=forms.Textarea)
    link = forms.CharField(label='ссылка (без меток)', 
                           max_length=500, required=False)
    utm = forms.BooleanField(label='Использовать метки', required=False, initial=True)

    state = forms.ModelMultipleChoiceField(queryset=State.objects.all())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
