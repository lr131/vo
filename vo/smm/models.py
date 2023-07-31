from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings
from .const import MAILING_SOURCE_TYPES, MAILING_RESULT_CHOISES, SOURCE_MAILING_STATE
import uuid
import urllib.parse


class AuthData(models.Model):
    social = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, blank=True, null=True)
    phone_own = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.social
    
    class Meta:
        verbose_name = 'Доступ'
        verbose_name_plural = 'Доступы'

# Это вид контента: информационный, развлекательный, анонс и тд
class ContentType(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Тип контента'
        verbose_name_plural = 'Типы контента'
        db_table = 'content_type'

    def __str__(self):
        return self.name
  
# где размещаем: сторис, посты, рилс, клипы
class ContentPlace(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Способ размещения контента'
        verbose_name_plural = 'Способы размещения контента'
        db_table = 'content_place'

    def __str__(self):
        return self.name

# Видео, аудио, текст
class ContentFormat(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Вид контента'
        verbose_name_plural = 'Виды контента'
        db_table = 'content_format'

    def __str__(self):
        return self.name

# Стаьтя, лонгрид, короткий пост, картинка, карусель, кружочек, голосовое, подкаст и тд?
class ContentForm(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Формат контента'
        verbose_name_plural = 'Форматы контента'
        db_table = 'content_form'

    def __str__(self):
        return self.name
       
# Цель поста: повысить охват, ещё что-нибудь такое 
class Target(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'Цель поста'
        verbose_name_plural = 'Цели поста'
        db_table = 'target'

    def __str__(self):
        return self.name

# рубрика
class Rubric(models.Model):
    name = models.CharField(max_length=300)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        db_table = 'rubric'

    def __str__(self):
        return self.name
    
      
class UTMSource(models.Model):
    social = models.CharField(max_length=200)
    utm_source = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.social
    
    class Meta:
        verbose_name = 'UTMSource'
        verbose_name_plural = 'Список UTMSource'
    
class Medium(models.Model):
    type_source = models.CharField(max_length=200)
    utm_medium = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    enable = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, 
                              null=True, blank=True,
                              verbose_name="чья метка (из команды)")

    def __str__(self):
        return self.utm_medium
    
    class Meta:
        verbose_name = 'UTMMedium'
        verbose_name_plural = 'Метки UTMMedium'

class CampaingUTM(models.Model):
    type_source = models.CharField(max_length=200)
    utm_campaign = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.utm_campaign
    
    class Meta:
        verbose_name = 'UTMCampaign'
        verbose_name_plural = 'Метки UTMCampaign'
        db_table = 'smm_utm_campaing'
        

class TypeSourceUTM(models.Model):
    title = models.CharField(max_length=200)
    utm_type_source = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    enable = models.BooleanField(default=True)


    def __str__(self):
        return self.utm_type_source
    
    class Meta:
        verbose_name = 'UTM Type Source (тип ресурса, группа, канал, сообщение или что)'
        verbose_name_plural = 'Метки UTM Type Source'
        db_table = 'smm_utm_type_source'
        

class TypeContentUTM(models.Model):
    title = models.CharField(max_length=200)
    utm_type_content = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    enable = models.BooleanField(default=True)


    def __str__(self):
        return self.utm_type_content
    
    class Meta:
        verbose_name = 'UTM Type Content (post/stories/header)'
        verbose_name_plural = 'Метки UTM Type Content'
        db_table = 'smm_utm_type_Content'
            

class Links(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True) # Дата создания ссылки
    link = models.CharField(max_length=200) # длинная ссылка
    short = models.CharField(max_length=200, blank=True, null=True) # сокращенная ссылка
    source = models.CharField(max_length=200) # источник
    utm_source = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_source")
    utm_type_source = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_type_source")
    utm_medium = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_medium")
    utm_type_content = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_type_content")
    utm_campaign = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_campaign")
    utm_term = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_term")
    utm_content = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_content")
    
    class Meta:
        verbose_name = 'Готовая ссылка с utm-метками'
        verbose_name_plural = 'Готовые ссылки с utm-метками'
        
    def __str__(self):
        return self.link
    
# Все наши места, где мы размещаемся
class SocialPlace(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=150, null=True, blank=True)
    social = models.CharField(max_length=20)
    utm_source = models.ForeignKey(UTMSource, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_source (Соцсеть или месседжер)")
    utm_type_source = models.ForeignKey(TypeSourceUTM, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_type_source (группа/страница/канал/чат/direct)",)
    utm_medium = models.ForeignKey(Medium, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_medium (Тип трафика)")
   
    class Meta:
        verbose_name = 'Место размещения (соцсеть или лэндинг)'
        verbose_name_plural = 'Места размещения (соцсети и сайты)'
        db_table = 'social_place'

    def __str__(self):
        return self.name
    
class UTMs(models.Model):
    utm_source = models.ForeignKey(UTMSource, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_source (Источник кампании)")
    utm_type_source = models.ForeignKey(TypeSourceUTM, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_type_source (группа/страница/канал/чат/direct)",)
    utm_medium = models.ForeignKey(Medium, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_medium (Тип трафика)")
    utm_type_content = models.ForeignKey(TypeContentUTM, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_type_content (Тип контента)")
    utm_campaign = models.ForeignKey(CampaingUTM, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_campaign (Название кампании))")
    
    class Meta:
        verbose_name = 'Готовый набор UTM меток'
        verbose_name_plural = 'Готовый набор UTM меток'
        db_table = 'smm_utms'
        
    def __str__(self):
        return f"{self.utm_source}-{self.utm_type_source}-{self.utm_medium}-{self.utm_type_content}-{self.utm_campaign}"

class PostType(models.Model):
    post_type = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=800, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Тип поста'
        verbose_name_plural = 'Типы постов'
        
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    class Meta:
        verbose_name = 'Теги к постам (для внутр.использования!!)'
        verbose_name_plural = 'Теги к постам (для внутр.использования!!)'
        
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name 

    
class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата создания поста")
    create_user = models.CharField(max_length=200, blank=True, null=True) # TODO поменять тип
    modify_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата редактирования поста")
    modify_user = models.CharField(max_length=200, blank=True, null=True, verbose_name="Кто редактировал пост") # TODO поменять тип
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_content = models.CharField(max_length=800, blank=True, null=True, verbose_name="Кратко - о чем")
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Тип поста") # TODO проверить тип
    description = models.CharField(max_length=800, blank=True, null=True, verbose_name="Описание")
    text = models.TextField(max_length=4800, blank=True, null=True, verbose_name="Пост")
    attachments = models.CharField(max_length=200, blank=True, null=True, verbose_name="Вложения") # TODO поменять тип
    performer = models.ManyToManyField(User, blank=True, verbose_name="Исполнитель(-и)")
    target_fk = models.ForeignKey(Target, db_column='target_fk', on_delete=models.SET_NULL,  null=True, verbose_name="Цель поста")
    rubric_fk = models.ForeignKey(Rubric, db_column='rubric_fk', on_delete=models.SET_NULL,  null=True, verbose_name="Рубрика")
    content_place_fk = models.ForeignKey(ContentPlace, db_column='content_place_fk', on_delete=models.CASCADE, verbose_name="Где размещать")
    content_form_fk = models.ForeignKey(ContentForm, db_column='content_form_fk', on_delete=models.CASCADE,verbose_name="Формат контента")
    content_format_fk = models.ForeignKey(ContentFormat, db_column='content_format_fk', on_delete=models.CASCADE, verbose_name="Вид контента")
    content_type_fk = models.ForeignKey(ContentType, db_column='content_type_fk', on_delete=models.CASCADE, default=1, verbose_name="Тип контента")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    
    class Meta:
        verbose_name = 'База постов'
        verbose_name_plural = 'База постов'
    
    def __str__(self):
        return self.short_content


class PostPlan(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост") # TODO проверить тип
    source = models.ForeignKey(Medium, on_delete=models.CASCADE, verbose_name="Метка utm_source места публикации") # TODO проверить тип и указать, что это - место публикации
    pub_date = models.DateTimeField(blank=True, null=True, verbose_name="Когда опубликовать") 
    deadline_date = models.DateTimeField(null=True, blank=True, verbose_name="Крайний срок, дедлайн")
    disable_date = models.DateTimeField(blank=True, null=True, verbose_name="дата отмены поста") # дата отмены поста 
    state = models.CharField(max_length=200, blank=True, null=True, verbose_name="Стадия поста") # Состояние: в работе, опубликован, не опубликован, перенесен
    reasons = models.CharField(max_length=200, blank=True, null=True, verbose_name="Причина отмены публикации") # Причина отмены публикации
    is_published = models.BooleanField(default=False, verbose_name="Пост опубликован")
    link = models.TextField(blank=True, null=True, verbose_name="Ссылка на пост")
    
    class Meta:
        verbose_name = 'Контент-план'
        verbose_name_plural = 'Контент-план'


class SourceMailing(models.Model):
    name = models.CharField(max_length=200)
    utm_source = models.ForeignKey(UTMSource, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_source (Соцсеть или месседжер)")
    utm_medium = models.ForeignKey(Medium, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_medium (Тип трафика)")
    utm_campaign = models.ForeignKey(CampaingUTM, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_campaign (Название кампании))")
    price = models.DecimalField(default=0, 
                                max_digits = 5,
                                decimal_places = 2,
                                verbose_name="Стоимость размещения")
    description = models.CharField(max_length=2000, 
                                   verbose_name="Короткое описание источника")
    state = models.CharField(max_length=10,
                            choices=SOURCE_MAILING_STATE,
                            default='actual')
    
    class Meta:
        verbose_name = 'Внешний ресурс для размещения'
        verbose_name_plural = 'Внешние ресурсы для размещения'

    def __str__(self):
        return f"{self.name} ({self.utm_source})"

class State(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'client_state'

    def __str__(self):
        return self.name

class Client(models.Model):
    family = models.CharField(max_length=250, null=True)
    name = models.CharField(max_length=250, null=True)
    patr = models.CharField(max_length=250, null=True, blank=True)
    birthday = models.DateTimeField(blank=True, null=True,
                                    default=datetime(1900, 1, 1, hour=16))
    city = models.CharField(max_length=250, null=True)
    in_black_list = models.BooleanField(default=False,
                                        verbose_name="В черном списке")
    state = models.ForeignKey(State, 
                              on_delete=models.SET_NULL, 
                              null=True, blank=True, 
                              default=8,
                              verbose_name="Статус")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарии")
    note = models.TextField(null=True, blank=True, verbose_name="Заметки") # заметки, дополнительно
    group = models.CharField(max_length=10, default='irk', verbose_name="База",)
    working = models.CharField(max_length=250,
                               null=True, blank=True,
                               verbose_name="Сфера деятельности",)
    have_kids = models.BooleanField(default=False, verbose_name="Есть дети",)
    kids = models.CharField(max_length=1000, 
                            null=True, blank=True,
                            verbose_name="Дети, подробности",)
    class Meta:
        managed = False
        db_table = 'clients_client'
        
    def __str__(self):
        return f"{self.family} {self.name} ({self.city})"
    
    @property
    def fio(self):
        return f"{self.family} {self.name} {self.patr if self.patr else ''}"

class ClientProducts(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='products')
    is_assisting = models.BooleanField(default=False,verbose_name="Клиент ассистировал") # Клиент уже ассистировал на БК
    future_assisting = models.BooleanField(default=False, verbose_name="Хочет на ассистирование") # клиент хочет на будущие ассистирования
    is_base_course = models.BooleanField(default=False,verbose_name="Курсовой")
    course_candidate = models.TextField(null=True, blank=True,verbose_name="Кандидаты на курс")
    is_school_level_1 = models.BooleanField(default=False,verbose_name="Выпускник ИШ1")
    is_school_level_2 = models.BooleanField(default=False,verbose_name="Выпускник ИШ2")
    is_school_level_3 = models.BooleanField(default=False, verbose_name="Выпускник ИШ3")
    tg = models.BooleanField(default=False,verbose_name="Выпускник терапевтической группы") # Клиент проходил терапевтическую группу
    
    class Meta:
        managed = False
        db_table = 'client_products'
    
    def __str__(self):
        return (f" {self.client.family} " if self.client.family else ""
                f"{self.client.name} " if self.client.name else ""
                f"{self.course_candidate}" if self.course_candidate else "")


class ClientMailing(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='mailing')
    viber_group = models.BooleanField(default=False, verbose_name="Группа в viber")
    tg_group = models.BooleanField(default=False, verbose_name="Группа в тг")
    wa_group = models.BooleanField(default=False, verbose_name="Группа в whatsapp")
    viber = models.BooleanField(default=False)
    tg = models.BooleanField(default=False, verbose_name="telegram")
    wa = models.BooleanField(default=False, verbose_name="whatsapp")
    sms = models.BooleanField(default=False,verbose_name="смс")
    call = models.BooleanField(default=False,verbose_name="Звонить")
    comment = models.TextField(null=True, blank=True,verbose_name="Примечания")
    
    class Meta:
        managed = False
        db_table = 'client_mailing'

    def __str__(self):
        return (f" {self.client.family} " if self.client.family else ""
                f"{self.client.name} " if self.client.name else ""
                f"{self.comment}" if self.comment else "")

class Place(models.Model):
    addr = models.CharField(max_length=200,null=True,blank=True, verbose_name="Адрес")
    source =  models.CharField(max_length=200,null=True,blank=True, verbose_name="Название") # онлайн, зал, кабинет
    
    class Meta:
        managed = False
        db_table = 'events_place'
        
    def __str__(self) -> str:
        return f"{self.addr}"
    
class EventState(models.Model):
    name = models.CharField(max_length=300, verbose_name="Статус")
    description = models.CharField(max_length=200,null=True,blank=True, verbose_name="Описание")
    
    class Meta:
        managed = False
        db_table = 'event_state'
        
    def __str__(self) -> str:
        return f"{self.name}"


class EventType(models.Model):
    name = models.CharField(max_length=300, verbose_name="Тип мероприятия")
    description = models.CharField(max_length=200,null=True,blank=True, verbose_name="Описание")
    
    class Meta:
        managed = False
        db_table = 'event_types'
        
    def __str__(self) -> str:
        return f"{self.name}"

class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    state = models.ForeignKey(EventState, verbose_name="Статус", null=True, blank=True, on_delete=models.SET_NULL) # проводится, не проводится, в архиве и тд
    event_type = models.ForeignKey(EventType, verbose_name="Тип мероприятия",  null=True, blank=True, on_delete=models.SET_NULL) # Тренинг, программа, марафон и тд
    description = models.TextField(null=True,blank=True, verbose_name="Описание")
    short = models.CharField(max_length=500, blank=True, null=True, verbose_name="Короткое описание (до 500 знаков)")
    payment = models.CharField(max_length=200,null=True,blank=True, verbose_name="Стоимость")
    continuance = models.CharField(max_length=200,null=True,blank=True, verbose_name="Продолжительность") # продолжительность
    about = models.TextField(null=True,blank=True, verbose_name="Какие боли закрывает?") # какие боли закрывает
    country = models.IntegerField(default=5, verbose_name="Сколько человек по плану") # количество человек по плану
    next_step = models.TextField(null=True,blank=True, verbose_name="Следующий шаг по продуктам") # следующий шаг по продуктам TODO
    prev_step = models.TextField(null=True,blank=True, verbose_name="Предыдущий шаг по продуктам") # предыдущий шаг / бесплатные материалы TODO
    created_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата создания")
    site = models.CharField(max_length=500, null=True, blank=True, verbose_name="Ссылка на лендинг")
    
    class Meta:
        managed = False
        db_table = 'events_event'
        
    def __str__(self) -> str:
        return f"{self.name} ({self.event_type}) - {self.state}"

class EventPlan(models.Model):
    start_date = models.DateTimeField(blank=True, verbose_name="Дата начала")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата завершения")
    season = models.CharField(max_length=100, default="2023/2024", verbose_name="Сезон")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Мероприятие")
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Где")
    is_period = models.BooleanField(default=False, verbose_name="Это периодичное мероприятие?")
    site = models.CharField(max_length=500, null=True, blank=True, verbose_name="Ссылка на лендинг (перекроет ссылку тренинга)")
    period = models.PositiveIntegerField(null=True,blank=True, verbose_name="Введите период (в днях)") # через сколько дней если что повторять
    
    class Meta:
        managed = False
        db_table = 'event_plan'
    
    def __str__(self):
        return (f" {self.event.name} " if self.event.name else ""
                f"{self.place} " if self.place else ""
                f"{self.start_date}" if self.start_date else "")


class Mailing(models.Model):
    name = models.CharField(max_length=100, 
                            verbose_name="Название рассылки")
    description = models.CharField(max_length=100, 
                            verbose_name="Описание рассылки")
    event_plan_id = models.ForeignKey(EventPlan, on_delete=models.SET_NULL, 
                                      null=True, blank=True, verbose_name="По поводу мероприятия")
    text = models.TextField(blank=True, null=True, verbose_name="текст рассылки без меток")
    source_type = models.CharField(max_length=100,
                                   choices=MAILING_SOURCE_TYPES,
                                   default='group',
                                   verbose_name="Тип рассылки")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = 'Список для рассылки'
        verbose_name_plural = 'Список рассылок'

    def __str__(self):
        return f"{self.name}"

class Lid(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    lid_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Код заявки")
    block_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Код блока")
    form_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Форма на сайте")
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name="Имя")
    phone = models.CharField(max_length=250, blank=True, null=True, verbose_name="Телефон")
    email = models.CharField(max_length=250, blank=True, null=True, verbose_name="Почта")
    utm_source = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_source")
    utm_type_source = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_type_source")
    utm_medium = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_medium")
    utm_type_content = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_type_content")
    utm_campaign = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_campaign")
    utm_term = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_term")
    utm_content = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_content")
    client_id = models.IntegerField(blank=True, null=True, verbose_name="Клиент (если новый, то пусто)")
    event_id = models.IntegerField(blank=True, null=True, verbose_name="Мероприятие (пусто, если клиент не знает чего хочет")
    action = models.CharField(max_length=250, verbose_name="Действие: позвонил, написал, оставил заявку через сайт и тд")
    source = models.CharField(max_length=250, verbose_name="Источник связи, ссылка")
    comment = models.TextField(blank=True, null=True, verbose_name="Примечания (внутренние)")
    target = models.CharField(blank=True, null=True, max_length=250, verbose_name="Целевое действие") # купил курс, зашел на марафон и тд
    
    class Meta:
        managed = False
        db_table = 'lid'
        
    def __str__(self):
        return f'{self.name} ({self.form_name}) {self.date}'
    
class MailingDetail(models.Model):
    mailing = models.ForeignKey(Mailing,
                                on_delete=models.CASCADE,
                                null=True, blank=True)
    
    source = models.ForeignKey(SourceMailing, 
                               on_delete=models.RESTRICT,
                               null=True, blank=True,
                               verbose_name="Источник указываем для групп")
    text = models.TextField()
    link = models.CharField(max_length=500, null=True, blank=True,
                            verbose_name="Ссылка, если есть, без меток")
    outer_text = models.TextField(verbose_name="Готовый текст для whatsapp, сформируется автоматически")
    outer_text_vi = models.TextField(null=True, blank=True,
                                     verbose_name="Готовый текст для viber, сформируется автоматически")
    outer_text_tg = models.TextField(null=True, blank=True,
                                     verbose_name="Готовый текст для viber, сформируется автоматически")
    
    cdate = models.DateTimeField(auto_now_add=True)
    cuser = models.ForeignKey(settings.AUTH_USER_MODEL, 
                              on_delete=models.RESTRICT,
                              related_name='smm_cuser')
    
    mdate = models.DateTimeField(auto_now=True)
    muser = models.ForeignKey(settings.AUTH_USER_MODEL, 
                              on_delete=models.RESTRICT,
                              related_name='smm_muser')
    
    pdate = models.DateTimeField(verbose_name="Дата выполнения",
                                 null=True, blank=True)
    puser = models.ForeignKey(User, on_delete=models.RESTRICT, 
                              null=True, blank=True,
                              verbose_name="Кто выполнил",
                              related_name='smm_puser')
    
    link_messeger = models.TextField(null=True, blank=True,
                                     verbose_name="Месседжер")
    client = models.ForeignKey(Client, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="Клиент")
    phone = models.CharField(max_length=20, null=True, blank=True,
                                    verbose_name="Номер телефона клиента")
    result = models.CharField(max_length=100,
                                   choices=MAILING_RESULT_CHOISES,
                                   default='Ожидает отправки')
    lid_id = models.ForeignKey(Lid, on_delete=models.SET_NULL,
                               null=True, blank=True,verbose_name="Связь с заявкой")
    comment = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Клиент в рассылке'
        verbose_name_plural = 'Клиенты в рассылках'

    def __str__(self):
        
        s = []
        s.append(f"{self.mailing.name} ({self.mailing.description}) ")
        if self.pdate:
            s.append(f"{self.pdate:%d.%m.%Y} ")
        s.append(f"{self.client} | ")
        if self.link_messeger:
            s.append(f"{self.link_messeger} - ")
        s.append(f"{self.result}")
        if self.comment:
            s.append(f"({self.comment})")
        return ''.join(s)
        # return (f"{self.mailing}"
        #         f"{self.pdate:%d.%m.%Y} " if self.pdate else ""
        #         f"{self.client} | "
        #         f"{self.link_messeger} - " if self.link_messeger else ""
        #         f"{self.result}"
        #         f"({self.comment})" if {self.comment} else ""
        #         )
    
    @property
    def link_wa_pc(self):
        query = {
            'text': f"{self.outer_text}"
        }
        params = urllib.parse.urlencode(query)
        return f'https://web.whatsapp.com/send/?phone={self.phone}&{params}&type=phone_number&app_absent=0'
    
    @property
    def link_wa(self):
        query = {
            'text': f"{self.outer_text}"
        }
        params = urllib.parse.urlencode(query)
        return f"https://wa.me/{self.phone}?{params}"
    
    @property
    def link_vi(self):
        # https://viber.click/номертелефона
        # <a href="viber://chat?number=%2B79501476150">Viber</a>
        return f"viber://chat?number=%2B{self.phone}"
    
    @property
    def link_tg(self):
        # https://t.me/+79834631106
        # tg://resolve?domain=username
        return f"https://t.me/+{self.phone}"