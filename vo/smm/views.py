from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import FileResponse, HttpResponse
import pandas as pd
import io
import os
from furl import furl

from .forms import MailingForm, MailindBDForm, MailingDetailForm, SocialPlaceForm, LinksForm, LinkSpeedForm, MailindQuickDetailForm, UploadWapicoReportForm, LinkSetForm


from .models.links import Links
from .models.social_place import SocialPlace
from .models.utms import UTMs
from .models.client import Client

from .models.mailing import Mailing
from .models.mailing_detail import MailingDetail

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
    data = Mailing.objects.all().order_by('-date')
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
    data = Links.objects.all().order_by('-date')
    context = {'data': data,}
    return render(request, 'smm/links/links_list.html', context=context)

@login_required
def link_new(request):
    if request.method == "POST":
        form = LinkSetForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data['source']
            utm_term = form.cleaned_data['utm_term']
            utm_content = form.cleaned_data['utm_content']
            
            site = source.site
            if not site:
                site = source.event.site
            utms_set = UTMs.objects.all()
            
            import vk_api
            login, password = settings.LOGIN_VK, settings.PASSWORD_VK
            scope = 4096
            vk_session = vk_api.VkApi(login=login, password=password, app_id=2685278, scope=scope)

            try:
                vk_session.auth(token_only=True)
            except vk_api.AuthError as error_msg:
                print(error_msg)
                raise 
            
            vkapi = vk_session.get_api()
            
            for utms in utms_set:
                utm_source_name = utms.utm_source.social if utms.utm_source else ''
                utm_type_source_name = utms.utm_type_source.title if utms.utm_type_source else ''
                utm_medium_name = utms.utm_medium.type_source if utms.utm_medium else ''
                utm_type_content_name = utms.utm_type_content.title if utms.utm_type_content else ''
                utm_campaign_name = utms.utm_campaign.type_source if utms.utm_campaign else ''
                
                source_name = "".join((f"Соцсеть-источник: {utm_source_name}\n" if utm_source_name else "",
                                      f"Тип источника: {utm_type_source_name}\n" if utm_type_source_name else "",
                                      f"Чей ресурс: {utm_medium_name}\n" if utm_medium_name else "",
                                      f"Тип контента: {utm_type_content_name}\n" if utm_type_content_name else "",
                                      f"Название кампании: {utm_campaign_name}\n " if utm_campaign_name else ""))
                
                link = "".join((f"{site}?",
                        f"utm_source={utms.utm_source.utm_source}&" if utms.utm_source else "",
                        f"utm_type_source={utms.utm_type_source.utm_type_source}&" if utms.utm_type_source else "",
                        f"utm_medium={utms.utm_medium.utm_medium}&" if utms.utm_medium else "",
                        f"utm_type_content={utms.utm_type_content.utm_type_content}&" if utms.utm_type_content else "",
                        f"utm_campaign={utms.utm_campaign.utm_campaign }&" if utms.utm_campaign else "",
                        f"utm_term={utm_term}&" if utm_term else "",
                        f"utm_content={utm_content}&" if utm_content else "",
                        ))
                
                link = link[:len(link) - 1]  
                
                link_params = {"link": link,
                               "utm_source": utms.utm_source.utm_source if utms.utm_source else '-',
                               "utm_type_source": utms.utm_type_source.utm_type_source if utms.utm_type_source else '-',
                               "utm_medium": utms.utm_medium.utm_medium if utms.utm_medium else '-',
                               "utm_type_content": utms.utm_type_content.utm_type_content if utms.utm_type_content else '-',
                               "utm_campaign": utms.utm_campaign.utm_campaign if utms.utm_campaign else '-',
                               "utm_term": utm_term if utm_term else '-',
                               "utm_content": utm_content if utm_content else '-'}    
                
                created = False
                try:
                    obj, created = Links.objects.get_or_create(**link_params)
                except Links.MultipleObjectsReturned as e:
                    objs = Links.objects.filter(**link_params)
                    obj = objs.first()
                    for v in objs:
                        if v.pk != obj.pk:
                            v.delete()
                    created = False
                finally:    
                    if created:
                        params = {'url': link, 'private': 1}
                        short = vkapi.utils.getShortLink(**params)
                        sh = short.get('short_url')
                    
                        print(link, sh, source_name)
                        
                        obj.short = sh
                        obj.source = source_name
                        obj.save()

            return redirect('smm:link_list')
    else:
        form = LinkSetForm()
    return render(request, 'smm/links/link_new.html', {'form': form})


@login_required
def mailing_group(request, pk):
    data = Mailing.objects.get(pk=pk)
    clients = MailingDetail.objects.filter(mailing=data)
    context = {'mailing': data, 'clients': clients}
    
    return render(request, 'smm/mailing/mailing_group.html', context=context)

@login_required
def get_mailing_db_file(request, pk):
    prev_url = furl(request.META.get('HTTP_REFERER'))
    filter = prev_url.args.get('filter')
    data = Mailing.objects.get(pk=pk)
    clients = MailingDetail.objects.filter(mailing=data)
    if filter:
        if filter == 'wait':
            clients = clients.filter(result='Ожидает отправки')
        elif filter == 'delivered':
            clients = clients.filter(result='Delivered')
        elif filter == 'read':
            clients = clients.filter(result='Read')
            
    data_to_df = []
    columns = ['Phone Number', 'Name','Last Name', 'State', 'City']
    
    for client in clients:        
        f = client.client.family if client.client.family else ""
        n = client.client.name if client.client.name else ""

        raw = (client.phone, n, f, client.client.state.name, client.client.city)
        data_to_df.append(raw)
            
    df_res = pd.DataFrame(data_to_df, columns=columns)
    
    with io.BytesIO() as b:
        # Use the StringIO object as the filehandle.
        writer = pd.ExcelWriter(b, engine='openpyxl')
        df_res.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.close()
        filename = data.name
        content_type = 'application/vnd.ms-excel'
        response = HttpResponse(b.getvalue(), content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
        return response

def handle_uploaded_file(f):
    path = os.path.join(settings.MEDIA_ROOT, 'smm')
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path,'report.xlsx')
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required
def mailing_db(request, pk):
    data = Mailing.objects.get(pk=pk)
    clients = MailingDetail.objects.filter(mailing=data)
    
    filter = request.GET.get("filter")
    if filter:
        if filter == 'wait':
            clients = clients.filter(result='Ожидает отправки')
        elif filter == 'delivered':
            clients = clients.filter(result='Delivered')
        elif filter == 'read':
            clients = clients.filter(result='Read')
    
    context = {'mailing': data, 'clients': clients}
    if request.method == 'POST':
        form = UploadWapicoReportForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            path = os.path.join(settings.MEDIA_ROOT, 'smm','report.xlsx')
            part = pd.read_excel(path, na_filter = False)
            
            if clients:
                for row in part.itertuples(index=False):
                    print(row)
                    phone = row[1]
                    try:
                        qs = clients.get(phone=int(phone))
                    except Exception:
                        print(phone, 'ошибка')
                        continue
                    print(qs)
                    qs.pdate = row[4]
                    qs.link_messeger = "WhatsApp"
                    qs.result = row[0]
                    if len(row[5]):
                        qs.comment = f"Ответное сообщение: \n{row[5]}"
                    qs.save()
            else:
                for row in part.itertuples(index=False):
                    print(row)   
                    phone = row[1] 
                    c = Client.objects.filter(phone__contains=str(phone)).first()
                    params = {
                        'pdate': row[4],
                        'link_messeger': "WhatsApp",
                        'result': row[0],
                        'text': "не доступен, так как данная рассылка уже сформирована из отчета",
                        'outer_text': "не доступен",
                        'phone': int(phone)
                    }
                    if len(row[5]):
                       params['comment'] = f"Ответное сообщение: \n{row[5]}"
                    MailingDetail.objects.create(mailing=data,
                                             cuser=request.user,
                                             muser=request.user,
                                             client=c,
                                             **params)
                    
            return redirect('smm:mailing_db', pk=pk)
    form = UploadWapicoReportForm()
    context['form'] = form
    report = {'total': clients.count(),
              'read': clients.filter(result='Read').count(),
              'delivered': clients.filter(result='Delivered').count(),
              'wait': clients.filter(result='Ожидает отправки').count(),
              'answer': clients.filter(comment__isnull=False).count(),
              'send': clients.filter(result='Отправил').count()}
    context['report'] = report
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
            cleated_msg = form.cleaned_data['msg']
            msg = form.cleaned_data['msg']
            link = form.cleaned_data['link']
            utm = form.cleaned_data['utm']
            states = [state['id'] for state in state.values()]
            groups = (db,)
            text = msg
            params = {'link': link}  
            msg_tg = ''
            msg_vi = '' 
            
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

            # тут надо не ДОБАВИТЬ МЕТКИ, тут ИСПОЛЬЗОВАТЬ UTM/
            # ЗАТЕМ найти вот эти вот ссылки в базе (тогда нужен механизм создания ссылок-таки)
            # ЗАТЕМ, уже если вдруг ссылки не найдено, а галка стоит, то создать эту ссылку или ссылки
            if utm and link and len(link):
                links = Links.objects.filter(link__startswith=link, 
                                             utm_medium='ravnovesie_asia',
                                             utm_type_content='direct')
                # links = Links.objects.filter(link__startswith=link,
                #                              utm_type_content='direct')
                # TODO предполагается, что ссылки уже есть в базе

                links_dict = {}
                
                for l in links:

                    if l.utm_source == 'tg':
                        print('tg')
                        links_dict['tg'] = l.short
                        msg_tg = msg.replace('%Url%', links_dict['tg'])
                        print('msg:\n', msg)
                    if l.utm_source == 'viber':
                        print('viber')
                        links_dict['viber'] = l.short
                        msg_vi = msg.replace('%Url%', links_dict['viber'])
                        print('msg:\n', msg)
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
                params['text'] = text.replace('%Name%', client['name'])
                # TODO создание объекта рассылки
                cl = Client.objects.get(pk=client['id'])
                for phone in phones:
                    MailingDetail.objects.create(mailing=data,
                                             outer_text = msg2,
                                             outer_text_vi = msg_vi,
                                             outer_text_tg = msg_tg,
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

