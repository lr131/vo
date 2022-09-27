from django.shortcuts import render

def smm(request):
    projectsList = [
        {'id':'1',
            'title':'Онлайн-кинотеатр',
            'description':'Кинотеатр с самой полной библиотекой фильмов.'},
        {'id':'2',
        'title':'Платформа с ИТ-курсами',
        'description':'Курсы по фронтенду, бэкенду и мобильной разработке.'},
        {'id':'3',
        'title':'Рекрутинговый портал',
        'description':'Вакансии для специалистов экстра-класса.'},
      ]
    return render(request, 'projects.html', {'projects':projectsList})
