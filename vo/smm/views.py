from contextlib import redirect_stderr
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import MailingForm, MailindBDForm, MailingDetailForm, SocialPlaceForm, LinksForm, LinkSpeedForm, MailindQuickDetailForm
from .models import Mailing, MailingDetail, Client, ClientProducts, Links, SocialPlace

@login_required
def mailing_new(request):
    if request.method == "POST":
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            # mailing.author = request.user
            # mailing.published_date = timezone.now()
            mailing.save()
            return redirect('smm:mailing_list')
    else:
        form = MailingForm()
    return render(request, 'smm/mailing/mailing_new.html', {'form': form})


@login_required
def mailing_list(request):
    data = Mailing.objects.all()
    context = {'mailing': data}
    return render(request, 'smm/mailing/mailing_list.html', context=context)


@login_required
def sp_list(request):
    data = SocialPlace.objects.all()
    context = {'data': data}
    return render(request, 'smm/links/sp_list.html', context=context)

@login_required
def sp_new(request):
    if request.method == "POST":
        form = SocialPlaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('smm:sp_list')
    else:
        form = SocialPlaceForm()
    return render(request, 'smm/links/sp_new.html', {'form': form})

@login_required
def link_list(request):
    data = Links.objects.all()
    if request.method == 'POST':
        form = LinkSpeedForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            link = form.cleaned_data['link']
            source = form.cleaned_data['source']
            
            if source == 'inner_person':
                us = {'wa': "WhatsApp", 'viber': "Viber", 'tg': "Telegram"}
                medium = 'person'
                for s in us:
                    name2 = f'{name} для рассылки по базе в личку в {us[s]}'
                    link2 = f'{link}?utm_source={s}&utm_medium={medium}'
                    
                    import vk_api
                    login, password = settings.LOGIN_VK, settings.PASSWORD_VK
                    scope = 4096
                    vk_session = vk_api.VkApi(login=login, password=password,scope=scope)

                    try:
                        vk_session.auth(token_only=True)
                    except vk_api.AuthError as error_msg:
                        print(error_msg)
                        return

                    vkapi = vk_session.get_api()
                    params = {'url': link2, 'private': 1}
                    short = vkapi.utils.getShortLink(**params)
                    sh = short.get('short_url')
                    Links.objects.create(link=link2,
                                         short=sh,
                                         source=name2,
                                         utm_source=s,
                                         utm_medium=medium)
            return redirect('smm:link_list')
            
    form = LinkSpeedForm()
    context = {'data': data, 'form': form}
    return render(request, 'smm/links/links_list.html', context=context)

@login_required
def link_new(request):
    if request.method == "POST":
        form = LinksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('smm:link_list')
    else:
        form = LinksForm()
    return render(request, 'smm/links/link_new.html', {'form': form})

@login_required
def mailing_group(request, pk):
    data = Mailing.objects.get(pk=pk)
    clients = MailingDetail.objects.filter(mailing=data)
    context = {'mailing': data, 'clients': clients}
    return render(request, 'smm/mailing/mailing_group.html', context=context)

@login_required
def mailing_db(request, pk):
    data = Mailing.objects.get(pk=pk)
    clients = MailingDetail.objects.filter(mailing=data)
    context = {'mailing': data, 'clients': clients}
    return render(request, 'smm/mailing/mailing_db.html', context=context)

@login_required
def mailing_db_new(request, pk):
    data = Mailing.objects.get(pk=pk)
    if request.method == 'POST':
        form = MailindBDForm(request.POST)
        if form.is_valid():
            db = form.cleaned_data['db']
            filter = form.cleaned_data['filter']
            state = form.cleaned_data['state']
            msg = form.cleaned_data['msg']
            link = form.cleaned_data['link']
            utm = form.cleaned_data['utm']
            states = [state['id'] for state in state.values()]
            groups = (db,)
            comment = msg
            params = {'link': link}   
            qs = Client.objects.filter(group__in=groups).extra(
                select={'id': 'clients_client.id',
                    'phone': 'clients_client.phone',
                    'state_name': 'client_state.name',
                    'viber_group': 'client_mailing.viber_group',
                    'tg_group': 'client_mailing.tg_group',
                    'wa_group': 'client_mailing.wa_group',
                    'viber': 'client_mailing.viber',
                    'tg': 'client_mailing.tg',
                    'wa': 'client_mailing.wa',
                    'sms': 'client_mailing.sms',
                    'call': 'client_mailing.call',
                    'mailing': 'client_mailing.comment',
                    'is_assisting': 'client_products.is_assisting',
                    'future_assisting': 'client_products.future_assisting',
                    'is_base_course': 'client_products.is_base_course',
                    'course_candidate': 'client_products.course_candidate',
                    'is_school_level_1': 'client_products.is_school_level_1',
                    'is_school_level_2': 'client_products.is_school_level_2',
                    'is_school_level_3': 'client_products.is_school_level_3',
                    'ter_gr': 'client_products.tg'},
            tables=['client_state','client_mailing', 'client_products'],
            where=['clients_client.state_id=client_state.id',
                'clients_client.id=client_mailing.client_id',
                'clients_client.id=client_products.client_id']
                ).order_by('family','name')
            if filter:
                if filter == 'no_base_course':
                    qs = qs.filter(products__is_base_course=False)
                if filter == 'is_base_course':
                    qs = qs.filter(products__is_base_course=True)
                if filter == 'is_assisting':
                    qs = qs.filter(products__is_assisting=True)
                if filter == 'future_assisting':
                    qs = qs.filter(products__future_assisting=True)
                if filter == 'is_school_level_1':
                    qs = qs.filter(products__is_school_level_1=True)
                if filter == 'is_school_level_2':
                    qs = qs.filter(products__is_school_level_2=True)
            qs = qs.filter(state__in=states)

            if utm and link and len(link):
                links = Links.objects.filter(link__startswith=link, utm_medium='person')
                # TODO предполагается, что ссылки уже есть в базе

                links_dict = {}
                
                for l in links:
                    print(l.utm_source == 'tg')
                    print(l.utm_source == 'viber')
                    print(l.utm_source == 'wa')

                    if l.utm_source == 'tg':
                        print('tg')
                        links_dict['tg'] = l.short
                        msg_tg = msg.replace('%Url%', links_dict['tg'])
                        print('msg:\n', msg)
                        print('comment ДО')
                        print(comment)
                        comment = comment + f"<br/><br/>Текст для Telegram:<br/><br/>{msg_tg}<br/><br/>"
                        print('comment ПОСЛЕ')
                        print(comment)
                    if l.utm_source == 'viber':
                        print('viber')
                        links_dict['viber'] = l.short
                        msg_vi = msg.replace('%Url%', links_dict['viber'])
                        print('msg:\n', msg)
                        print('comment ДО')
                        print(comment)
                        comment = comment + f"<br/><br/>Текст для Viber:<br/><br/>{msg_vi}<br/><br/>"
                        print('comment ПОСЛЕ')
                        print(comment)
                    if l.utm_source == 'wa':
                        links_dict['wa'] = l.short
                        link = l.short   
                print(links_dict)             
                
            msg = msg.replace('%Url%', link)    
            
            
            for client in qs.values():
                if not client['phone']:
                    continue
                phones = client['phone'].split(';')
                msg2 = msg.replace('%Name%', client['name'])
                params['comment'] = comment.replace('%Name%', client['name'])
                # TODO создание объекта рассылки
                cl = Client.objects.get(pk=client['id'])
                for phone in phones:
                    MailingDetail.objects.create(mailing=data,
                                             text = msg2,
                                             outer_text = msg2,
                                             cuser=request.user,
                                             muser=request.user,
                                             client=cl,
                                             phone=phone,
                                             **params)
        return redirect('smm:mailing_db', pk=pk)    
        
    clients = MailingDetail.objects.filter(mailing=data)
    form = MailindBDForm()
    context = {'mailing': data, 'clients': clients, 'form': form}
    return render(request, 'smm/mailing/mailing_db_new.html', context=context)

@login_required
def mailing_myperson(request, pk):
    data = Mailing.objects.all()
    context = {'mailing': data}
    return render(request, 'smm/mailing/mailing_myperson.html', context=context)

