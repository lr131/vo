from django.contrib import admin

from .models.auth_data import AuthData

from .models.content_type import ContentType
from .models.content_place import ContentPlace
from .models.content_format import ContentFormat
from .models.content_form import ContentForm
from .models.target import Target
from .models.rubric import Rubric
from .models.utm_source import UTMSource
from .models.utm_medium import Medium
from .models.utm_campaign import CampaingUTM
from .models.utm_type_source import TypeSourceUTM
from .models.utm_type_content import TypeContentUTM
from .models.links import Links
from .models.social_place import SocialPlace
from .models.utms import UTMs
from .models.post_type import PostType
from .models.tag import Tag
from .models.post import Post
from .models.content_plan import PostPlan

from .models.client_state import State
from .models.client import Client
from .models.client_product import ClientProducts
from .models.client_mailing import ClientMailing

from .models.event_place import Place
from .models.event_state import EventState
from .models.event_type import EventType
from .models.event import Event
from .models.event_plan import EventPlan

from .models.lid import Lid
from .models.mailing import Mailing
from .models.source_mailing import SourceMailing
from .models.mailing_detail import MailingDetail

class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    
    
class SocialPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'social', 'link')
    
    
class UTMSourceAdmin(admin.ModelAdmin):
    list_display = ('social', 'utm_source', 'description')
    

class MediumAdmin(admin.ModelAdmin):
    list_display = ('type_source', 'utm_medium', 'description', 'enable')
    
class CampaingUTMAdmin(admin.ModelAdmin):
    list_display = ('type_source', 'utm_campaign', 'description', 'enable')
    
class UTMsAdmin(admin.ModelAdmin):
    list_display = ('utm_source', 'utm_type_source', 'utm_medium', 'utm_type_content', 'utm_campaign')
    

class PostTypeAdmin(admin.ModelAdmin):
    list_display = ('post_type', 'name', 'description')


admin.site.register(AuthData)
admin.site.register(UTMSource, UTMSourceAdmin)
admin.site.register(Medium, MediumAdmin)
admin.site.register(CampaingUTM, CampaingUTMAdmin)
admin.site.register(UTMs, UTMsAdmin)
admin.site.register(TypeContentUTM)
admin.site.register(TypeSourceUTM)
admin.site.register(Links)
admin.site.register(Target)
admin.site.register(Rubric)
admin.site.register(PostType, PostTypeAdmin)
admin.site.register(Post)
admin.site.register(PostPlan)
admin.site.register(ContentFormat)
admin.site.register(ContentForm)
admin.site.register(ContentType,ContentTypeAdmin)
admin.site.register(SocialPlace, SocialPlaceAdmin)
admin.site.register(ContentPlace)
admin.site.register(Tag)
admin.site.register(Mailing)
admin.site.register(MailingDetail)
admin.site.register(SourceMailing)
