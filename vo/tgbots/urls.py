from django.urls import path
from .views import message_history,message_history_all

urlpatterns = [
    path('message-history/<int:user_id>/', message_history, name='message_history'),
    path('message-history/', message_history_all, name='message_history_all'),
    path('', message_history_all, name='message_history_all'),
]