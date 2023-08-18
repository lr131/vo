from django import forms
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .const import MAILING_SOURCE_TYPES, MAILING_RESULT_CHOISES, SOURCE_MAILING_STATE

from .models.links import Links
from .models.social_place import SocialPlace


from .models.client_state import State

from .models.event_plan import EventPlan
from .models.event import Event

from .models.mailing import Mailing
from .models.mailing_detail import MailingDetail

from .models.utm_source import UTMSource
from .models.utm_type_source import TypeSourceUTM
from .models.utm_medium import Medium
from .models.utm_campaign import CampaingUTM
from .models.utm_type_content import TypeContentUTM

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
            

class EventPlaceChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.event.event_type.name} {obj.event.name} - {obj.start_date:%d.%m.%Y} ({obj.place})'

class EventChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.event.event_type.name} {obj.event.name} - {obj.start_date:%d.%m.%y} ({obj.place})'

class LinkSetForm(forms.Form):
    form = forms.CharField(label='Что это за форма',
                           max_length=50,
                           initial='LinkSetForm',
                           widget=forms.HiddenInput())
    down_date = timezone.now() - timedelta(days=1) # end_date__gte
    update = timezone.now() + timedelta(weeks=15) # start_date__lte

    one_time_qs = EventPlan.objects.filter(
        Q(site__isnull=False) | Q(event__site__isnull=False),
        is_period=False,
        end_date__gte=down_date,
        start_date__lte=update
    )
    
    # TODO выяснить, как же вывести вместе с группой
    qs = one_time_qs

    source = EventPlaceChoiceField(
        label='для чего ссылка',
        queryset=qs.order_by('start_date'),
        required=False
    )
    
    utm_term = forms.CharField(label='Идентификатор объявления (utm_term)',
                               max_length=100, required=False)
    utm_content = forms.CharField(label='Ключевое слово (utm_content)',
                                  max_length=100, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UTMTypeSourceChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.title} ({obj.description})'
    
class UTMMediumChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        if obj.description:
            return f'{obj.type_source} ({obj.description})'
        else:
            return f'{obj.type_source}'

class LinkForm(forms.Form):
    form = forms.CharField(label='Что это за форма',
                           max_length=50,
                           initial='LinkForm',
                           widget=forms.HiddenInput())
    down_date = timezone.now() - timedelta(days=1)# end_date__gte
    update = timezone.now() + timedelta(weeks=15) # start_date__lte
    
    regular_qs = EventPlan.objects.filter(
        Q(site__isnull=False) | Q(event__site__isnull=False),
        is_period=True,
        end_date__gte=down_date,
        start_date__lte=update
    ).values('event').distinct()
    
    print(regular_qs)
    

    one_time_qs = EventPlan.objects.filter(
        Q(site__isnull=False) | Q(event__site__isnull=False),
        is_period=False,
        end_date__gte=down_date,
        start_date__lte=update
    )
    
    print(one_time_qs)
    
    print(regular_qs.count()) #1
    print(one_time_qs.count()) #25

    qs = regular_qs.union(one_time_qs)
    print(qs) #15

    # qs = sorted(qs, key=lambda obj: obj['start_date'], reverse=True)[:1]

    # TODO выяснить, как же вывести вместе с группой
    # qs = EventPlan.objects.filter(event__in=qs)
    qs = one_time_qs

    source = EventPlaceChoiceField(
        label='для чего ссылка',
        queryset=qs.order_by('start_date'),
        required=False
    )
    source_2 = forms.CharField(label='Для чего ссылка', required=False)
    utm_source = forms.ModelChoiceField(label='utm_source', 
                          queryset=UTMSource.objects.all().order_by('social')
                          )
    utm_type_source = UTMTypeSourceChoiceField(label='utm_type_source', 
                                             queryset=TypeSourceUTM.objects.filter(
                                                 enable=True).order_by('title'))
    utm_medium = UTMMediumChoiceField(label='utm_medium', 
                                             queryset=Medium.objects.filter(
                                                 enable=True).order_by('type_source'))
    utm_campaign = UTMMediumChoiceField(label='utm_campaign', 
                                             queryset=CampaingUTM.objects.all().order_by('type_source'))
    utm_type_content = UTMTypeSourceChoiceField(label='utm_type_content', 
                                             queryset=TypeContentUTM.objects.all().order_by('title'))
    utm_term = forms.CharField(label='Идентификатор объявления (utm_term)',
                               max_length=100, required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'free, -30%, registration'}))
    utm_content = forms.CharField(label='Ключевое слово (utm_content)',
                                  max_length=100, required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'link, landing page'}))
    
    def clean(self):
        cleaned_data = super().clean()
        field1_value = cleaned_data.get('source')
        field2_value = cleaned_data.get('source_2')
        
        # Проверка, что хотя бы одно из полей field1 и field2 заполнено
        if not field1_value and not field2_value:
            raise forms.ValidationError('Необходимо заполнить хотя бы одно из полей ссылки')

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class LinkSearchForm(forms.Form):
    form = forms.CharField(label='Что это за форма',
                           max_length=50,
                           initial='LinkSearchForm',
                           widget=forms.HiddenInput())
    down_date = timezone.now() - timedelta(days=1)# end_date__gte
    update = timezone.now() + timedelta(weeks=15) # start_date__lte

    one_time_qs = EventPlan.objects.filter(
        Q(site__isnull=False) | Q(event__site__isnull=False),
        is_period=False,
        end_date__gte=down_date,
        start_date__lte=update
    )

    qs = one_time_qs

    source = EventPlaceChoiceField(
        label='Какая ссылка',
        queryset=qs.order_by('start_date'),
    )
    utm_source = forms.ModelChoiceField(label='utm_source', 
                          queryset=UTMSource.objects.all().order_by('social'),
                          required=False
                          )
    utm_medium = UTMMediumChoiceField(label='utm_medium', 
                                      required=False,
                                      queryset=Medium.objects.filter(
                                      enable=True).order_by('type_source'))
    
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
    filter = forms.CharField(label='Фильтр', 
                             widget=forms.Select(choices=CHOICES_FILTER), 
                             required=False)
    msg = forms.CharField(label='Шаблон текста', widget=forms.Textarea)
    link = forms.CharField(label='Ссылка без utm-меток', 
                           max_length=500, required=False)
    utm = forms.BooleanField(label='Использовать UTM-метки', required=False, initial=True)

    state = forms.ModelMultipleChoiceField(label='Статус клиентов',
                                           queryset=State.objects.all())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
