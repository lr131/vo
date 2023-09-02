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
    ordering = ['-start_date']
    list_display = ('get_dates','get_info', 'site', 'get_place', 'get_event_type')
    actions = ['sort_by_start_date', 'sort_by_site', 'sort_by_season']
    
    # Метод действия для сортировки по дате начала
    def sort_by_start_date(self, request, queryset):
        queryset = queryset.order_by('start_date')
        self.message_user(request, "Мероприятия отсортированы по дате начала")
    
    sort_by_start_date.short_description = "Сортировать по дате начала"

    # Метод действия для сортировки по полю site
    def sort_by_site(self, request, queryset):
        queryset = queryset.order_by('site')
        self.message_user(request, "Мероприятия отсортированы по полю site")

    sort_by_site.short_description = "Сортировать по site"
    

    # Метод действия для сортировки по сезону
    def sort_by_season(self, request, queryset):
        queryset = queryset.order_by('season')
        self.message_user(request, "Мероприятия отсортированы по сезону")

    sort_by_season.short_description = "Сортировать по сезону"

admin.site.register(Place, PlaceAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(EventState, EventStateAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventPlan, EventPlanAdmin)