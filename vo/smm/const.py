MAILING_SOURCE_TYPES = (
    ("inner_person", "Рассылка по базе"),
    # ("group", "Рассылка в группы"),
    # ("outer_person", "Рассылка во вне с моей личной ссылкой")
)

MAILING_RESULT_CHOISES = (
    ('Ожидает отправки', 'Ожидает отправки'),
    ('Отправил', 'Отправлено'),
    ('Delivered', 'Доставлено'),
    ('Read', 'Прочитано'),
    ('Размещено (для групп)', 'Размещено (для групп)'),
    ('Есть ответ', 'Есть ответ'),
    ('Номер тренинг-центра в ЧС', 'Номер тренинг-центра в ЧС'),
    ('Нет в месседжере', 'Нет в месседжере'),
    
)

SOURCE_MAILING_STATE = (
    ('actual', "актуально"),
    ('archive', "в архиве")
)

CHOICES_POST_STATE = (
        ('wait', 'Ожидает действий'),
        ('in_progress', 'В работе'),
        ('published', 'Опубликован'),
        ('not_published', 'Не опубликован'),
        ('moved', 'Перенесен'),
    )