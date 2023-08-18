from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

from django.http import HttpResponse
from django.conf import settings

import telebot

from .bots.lr131bot import bot as tg_lr131_bot
from .bots.psy20_intensive_bot import bot as psy20_intensive_bot
from .bots.psy20_marathon_bot import bot as psy20_marathon_bot

from .models.history import History

@csrf_exempt
def telegram_webhook_lr131bot(request):
    if request.method == 'POST':
        json_str = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        tg_lr131_bot.process_new_updates([update])
    return HttpResponse()

@csrf_exempt
def telegram_webhook_psy20_intensive(request):
    if request.method == 'POST':
        json_str = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        psy20_intensive_bot.process_new_updates([update])
    return HttpResponse()

@csrf_exempt
def telegram_webhook_psy20_marathon(request):
    if request.method == 'POST':
        json_str = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        psy20_marathon_bot.process_new_updates([update])
    return HttpResponse()


def message_history(request, user_id):
    # Получаем все записи истории сообщений для указанного пользователя
    history = History.objects.filter(user_id=user_id)

    # Передаем историю сообщений в шаблон для отображения
    return render(request, 'tgbots/message_history.html', {'messages': history})


def message_history_all(request):
    # Получаем уникальных пользователей и последние сообщения для каждого пользователя
    # используя агрегацию и операции .latest()
    history = History.objects.values('user_id').annotate(
        latest_message_id=Max('id')
    ).values('latest_message_id')
    
    latest_messages = History.objects.filter(id__in=history)
    
    # Передаем последние сообщения в шаблон для отображения
    return render(request, 'message_history.html', {'messages': latest_messages})