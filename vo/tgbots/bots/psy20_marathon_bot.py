from django.conf import settings
import telebot
import os

from ..models.history import History
from ..models.user import User
from ..models.bot import TGBot
from ..utils import is_phone, get_start_text980, check_phone_in_last_messages

bot = telebot.TeleBot(settings.PSY20_MARATHON_TOKEN)
text = get_start_text980()

botPsy20marathon = TGBot.objects.get(pk=3) # пока абсолютное значение

def send_message_to_telegram(chat_id, message):
    bot.send_message(chat_id=chat_id, text=message)

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    obj, created = User.objects.get_or_create(tgbot=botPsy20marathon, user_id=user_id, chat_id = message.chat.id)
    History.objects.create(user=obj, tgbot=botPsy20marathon, message='запуск или перезапуск бота', mtype='start')
    bot.send_message(message.chat.id, text, parse_mode='markdown')

@bot.message_handler(content_types=["text"])
def text_message(message):
    user_id = message.from_user.id
    obj, created = User.objects.get_or_create(tgbot=botPsy20marathon, user_id=user_id, chat_id = message.chat.id)
    user_path = os.path.join(settings.MEDIA_ROOT, "bots_data", botPsy20marathon.bot_name, f"{user_id}")
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    
    # При любом раскладе пишем, что пользователь написал нам
    History.objects.create(user=obj, tgbot=botPsy20marathon, message=message.text, mtype='text')
    reply = ''

    if is_phone(message.text):
        screenshot_files = [f for f in os.listdir(user_path) if f.endswith(".jpg")]

        if screenshot_files:
            reply = "Спасибо за регистрацию, дождитесь ссылки на канал."
        else:
            reply = "Пожалуйста, отправьте скриншот оплаты." 
    else:
        reply = "Извините, номер не распознан. \
            \n\nПришлите, пожалуйста, номер телефона без символов и пробелов. \n\nНапример, 89086434405"
    
    History.objects.create(user=obj, tgbot=botPsy20marathon, message=f"ВЫ: {reply}", mtype='text')
    
    bot.send_message(message.chat.id, reply, parse_mode='markdown')
    

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    obj, created = User.objects.get_or_create(tgbot=botPsy20marathon, user_id=user_id, chat_id = message.chat.id)
    user_path = os.path.join(settings.MEDIA_ROOT, "bots_data", botPsy20marathon.bot_name, f"{user_id}")
    
    # необходимо, чтобы сохранить относительный путь файла
    short_path = os.path.join("bots_data", botPsy20marathon.bot_name, f"{user_id}")
    if not os.path.exists(user_path):
        os.makedirs(user_path)
        
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    
    downloaded_file = bot.download_file(file_info.file_path)
    
    file_path = f"{user_path}/{user_id}_{file_id}.jpg"
    short_file_path = f"{short_path}/{user_id}_{file_id}.jpg"
    
    with open(file_path, "wb") as file:
        file.write(downloaded_file)
    
    History.objects.create(user=obj, tgbot=botPsy20marathon, message=f"{short_file_path}", mtype='photo')
    
    phone_exist = check_phone_in_last_messages(user_id, botPsy20marathon)
    
    if os.path.exists(phone_exist):
        reply = "Спасибо за регистрацию, дождитесь ссылки на канал."
    else:
        reply = "Пожалуйста, отправьте номер телефона, указанный при регистрации на интенсив."
    History.objects.create(user=obj, tgbot=botPsy20marathon, message=f"ВЫ: {reply}", mtype='text')
    bot.reply_to(message, reply)
    


@bot.message_handler(content_types=['document'])
def handle_document(message):
    bot.reply_to(message, "Извините, бот не поддерживает такой формат сообщений. Пожалуйста, отправьте текст или скриншот об оплате.")

