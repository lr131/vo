from django.contrib import admin
from .models import Lid, ClientEventHistory, WebHook

admin.site.register(Lid)
admin.site.register(WebHook)
admin.site.register(ClientEventHistory)
