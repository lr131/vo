from django.contrib import admin
from .models import AuthData, Mailing, UTMSource, Medium, Links, Target, Rubric
from .models import PostType, Post, PostPlan, ContentFormat, ContentForm
from .models import ContentType, SocialPlace, ContentPlace, Tag
from .models import  Mailing, MailingDetail, SourceMailing

class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    
    
class SocialPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'social', 'link')
    
    
class UTMSourceAdmin(admin.ModelAdmin):
    list_display = ('social', 'utm_source', 'description')
    

class MediumAdmin(admin.ModelAdmin):
    list_display = ('type_source', 'utm_medium', 'description', 'enable')
    

class PostTypeAdmin(admin.ModelAdmin):
    list_display = ('post_type', 'name', 'description')


admin.site.register(AuthData)
admin.site.register(UTMSource, UTMSourceAdmin)
admin.site.register(Medium, MediumAdmin)
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
