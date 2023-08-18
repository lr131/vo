from datetime import datetime, timedelta
from django.db.models import Q
from .models.history import History
import re

def is_phone(number):
    pattern = r'^(\+7|8)[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$'
    match = re.match(pattern, number)
    return bool(match)

def get_start_text():
    return 'Поздравляем, остался всего один шаг до вступления! \
            \n\nДля регистрации на онлайн-марафон «Психология чувств 2.0» переведите *590 рублей* по номеру телефона *89041378474 (сбер)*\
            \n\nНа имя *Буяхаева Елена Анатольевна* – руководитель нашего центра.\
            \n\nПРИ ПЕРЕВОДЕ НЕ ОСТАВЛЯЙТЕ КОММЕНТАРИИ\n\nПосле оплаты, пришлите, пожалуйста:\
            \n\n· *скриншот* чека об оплате\
            \n\n· и свой номер телефона *(только цифры)*, который вы указывали при регистрации на онлайн-*интенсив* «Психология чувств 2.0». \
            \n\nДалее мы добавлим вас в закрытый telegram-канал, где будет проходить онлайн-марафон. \
            \n\nЕсли возникнут вопросы, пишите администратору @ravnovesie38'
            

def check_phone_in_last_messages(user_id, tgbot):
    # Получаем текущую дату и время
    now = datetime.now()

    # Вычисляем дату и время, прошедшие две последние недели
    two_weeks_ago = now - timedelta(weeks=2)

    # Формируем фильтры для получения последних 5 сообщений от пользователя
    filters = Q(user_id=user_id) & Q(date_time__gte=two_weeks_ago) & Q(tgbot=tgbot)

    # Получаем последние 5 сообщений от пользователя
    last_messages = History.objects.filter(filters).order_by('-date_time')[:5]

    # Проверяем, содержится ли в сообщениях номер телефона
    for message in last_messages:
        if is_phone(message.message):
            return True

    return False