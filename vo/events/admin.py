from django.contrib import admin

from .models.place import Place
from .models.event_state import EventState
from .models.event import Event
from .models.event_plan import EventPlan
from .models.event_type import EventType
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('addr', 'source')

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'continuance', 'event_type', 'description', 'about', 'payment', 'site')

class EventStateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class EventPlanAdmin(admin.ModelAdmin):
    ordering = ['start_date']
    list_display = ('get_dates','get_info', 'site', 'get_place', 'get_event_type')

admin.site.register(Place, PlaceAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(EventState, EventStateAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventPlan, EventPlanAdmin)