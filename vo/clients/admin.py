from django.contrib import admin
from .models import ClientInterest, ClientMailing, ClientProducts, State, Client

class ClientAdmin(admin.ModelAdmin):
    ordering = ['family', 'name', 'city', 'group']
    search_fields = ('family','name', 'city', 'phone', 'group')
    list_display = ('get_state', 'get_abbr_fio', 'get_city', 'get_phone', 'get_notes')


class ClientProductsAdmin(admin.ModelAdmin):
    ordering = ['course_candidate']
    search_fields = ('client_id',)
    list_display = ('client', 'is_assisting', 
                    'future_assisting', 
                    'is_base_course',
                    'course_candidate',
                    'is_school_level_1',
                    'is_school_level_2',
                    'is_school_level_3',
                    'tg')



class ClientMailingAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ('client', 'get_msg_groups', 'get_messengers', 'comment')


class ClientInterestAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ('client', 'event', 'comment')


class StateAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ('name', 'description')

admin.site.register(State, StateAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientProducts, ClientProductsAdmin)
admin.site.register(ClientMailing, ClientMailingAdmin)
admin.site.register(ClientInterest, ClientInterestAdmin)