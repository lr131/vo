from django.contrib import admin
from .models import Lid, ClientEventHistory, WebHook, Action

class WebHookAdmin(admin.ModelAdmin):
    list_display = ('cdate', 'tranid', 'formname', 'name', 'phone')
    
class LidAdmin(admin.ModelAdmin):
    list_display = ('tranid', 'formname', 'name', 'phone', 'email', 'action', 'comment', 'client_id', 
                    'utm_source', 'utm_type_source', 'utm_medium', 'utm_type_content', 
                    'utm_campaign', 'utm_term', 'utm_content')
    
class ActionAdmin(admin.ModelAdmin):
    list_display = ('cdate', 'plc', 'lid_info', 'description', 'action', 'note', 'stage')

admin.site.register(Lid, LidAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(WebHook,WebHookAdmin)
admin.site.register(ClientEventHistory)
