from django.contrib import admin
from .models import Lid, ClientEventHistory, WebHook

class WebHookAdmin(admin.ModelAdmin):
    list_display = ('cdate', 'tranid', 'formname', 'name', 'phone')

admin.site.register(Lid)
admin.site.register(WebHook,WebHookAdmin)
admin.site.register(ClientEventHistory)
