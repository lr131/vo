from django.contrib import admin

from .models.user import User
from .models.bot import TGBot
from .models.history import History

admin.site.register(User)
admin.site.register(History)
admin.site.register(TGBot)