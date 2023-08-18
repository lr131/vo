from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import message_history,message_history_all

urlpatterns = [
    path('message-history/<int:bot>/<int:user_id>/', message_history, name='message_history'),
    path('message-history/', message_history_all, name='message_history_all'),
    path('', message_history_all, name='message_history_all'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)