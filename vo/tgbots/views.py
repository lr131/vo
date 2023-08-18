from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.conf import settings

import telebot
from telebot import types

import os
from datetime import datetime
import time

from .models.history import History
from .models.user import User
from .models.bot import TGBot
from .utils import is_phone, get_start_text

bot = telebot.TeleBot(settings.LR131_TOKEN)
text = get_start_text()
botLR131 = TGBot.objects.get(pk=1)

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    obj, created = User.objects.get_or_create(tgbot=botLR131, chat_id=user_id)
    History.objects.create(user=obj, tgbot=botLR131, message='запуск или перезапуск бота', mtype='start')
    bot.send_message(message.chat.id, text, parse_mode='markdown')

@bot.message_handler(content_types=["text"])
def echo_message(message):
    user_id = message.from_user.id
    obj, created = User.objects.get_or_create(tgbot=botLR131, chat_id=user_id)
    History.objects.create(user=obj, tgbot=botLR131, message=message.text, mtype='text')
    bot.send_message(message.chat.id, message.text)

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        json_str = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
    return HttpResponse()
