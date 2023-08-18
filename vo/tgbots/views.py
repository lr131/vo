from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.conf import settings

import telebot

from .bots.lr131bot import bot 

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        json_str = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
    return HttpResponse()
