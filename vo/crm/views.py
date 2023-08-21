from distutils.command import clean
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.decorators.http import require_POST
from rest_framework import viewsets, serializers, generics, filters
from pprint import pprint

from .forms import ClientEventHistoryForm, PreviousListForm, ActionForm, LidForm, AddClientsSetForm, AddClientsForm

from .models.previous_list_client import PreviousListClient
from .models.webhook import WebHook
from .models.client_event_history import ClientEventHistory
from .models.previous_list import PreviousList
from .models.action import Action
from .models.lid import Lid
from .models.client import Client

from .serializers import PreviousListClientSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import unquote
import re
import json

@csrf_exempt
def tilda_webhook(request):
    if request.method == 'POST':
        raw_string =request.body.decode('utf-8')
        split_string = raw_string.split('&')
        
        data_dict = {}
        for item in split_string:
            key, value = item.split('=')
            data_dict[key] = value
   

        decoded_dict = {}
        for key, value in data_dict.items():
            decoded_key = unquote(key)
            decoded_value = unquote(value)
            decoded_dict[decoded_key] = decoded_value
        
        decoded_dict['source_link'] = request.META.get('HTTP_REFERER')
            
        body = json.dumps(decoded_dict)
                
        phone_number = decoded_dict.get('Phone', None)
        if phone_number:
            phone_number = re.sub(r'\D', '', phone_number)
        
        name = decoded_dict.get('Name', None)
        if name:
            name = name.replace("+", " ")
            
        formname = decoded_dict.get('formname', None)
        if formname:
            formname = formname.replace("+", " ")
            
        WebHook.objects.create(body=body,
                               formid=decoded_dict.get('formid', None),
                               formname=formname,
                               tranid=decoded_dict.get('tranid', None),
                               name=name,
                               phone=phone_number)
        
        return HttpResponse("ok")
    else:
        return HttpResponse("not allowed")

@login_required
def add_visit(request):
    if request.method == "POST":
        form = ClientEventHistoryForm(request.POST)
        if form.is_valid():
            print(form)
            history = form.save()
            return redirect('crm:get_lists')
    else:
        context = {
            "form": ClientEventHistoryForm()
        }
    return render(request, "crm/add_visit.html", context)

@login_required
def add_prevlist(request):
    
    if request.method == "POST":
        form = PreviousListForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            prev_list = form.save(commit=False)
            prev_list.cuser = request.user
            # prev_list.date = timezone.now()
            prev_list.save()
            return redirect('crm:get_lists')
        else:
            print(form)
            context = {
                    "form": form
                }
    else:    
        context = {
                "form": PreviousListForm()
            }
    return render(request, "crm/add_prevlist.html", context)

@login_required
def get_lists(request):
    context = {
        "lists": PreviousList.objects.all()
    }
    return render(request, "crm/prevlists.html", context)

@login_required
def get_lids(request):
    
    
    tmp = Lid.objects.filter(lid_code__contains='5225056')
    
    person = Lid.objects.filter(utm_medium='person').values_list()
    print(person)
        
    statistics = tmp.values('utm_medium').annotate(count=Count('id')).order_by('-count')
    # statistics = Lid.objects.values('utm_medium').annotate(count=Count('id')).order_by('-count')
    
    print (len(statistics))
    for entry in statistics:
        utm_medium = entry['utm_medium']
        count = entry['count']
        print(f"utm_medium: {utm_medium}, count: {count}")
    
    # TODO фильтровать по воркерам, выводить те, что без них
    context = {
        "lids": Lid.objects.filter(worker__isnull=True).order_by('-date')[:100],
        "statistics": statistics,
        "total": len(statistics)
    }
    
    return render(request, "crm/lids.html", context)


@login_required
def get_stat(request):
    
    tmp = Lid.objects.filter(event_id=43)
    statistics = tmp.values('utm_medium').annotate(count=Count('id')).order_by('-count')
    
    for entry in statistics:
        utm_medium = entry['utm_medium']
        count = entry['count']
        print(f"utm_medium: {utm_medium}, count: {count}")
    
    context = {
        "statistics": statistics,
        "total": tmp.count()
    }
    
    return render(request, "crm/statistics.html", context)


@login_required
def add_lid(request):
    clid = request.GET.get("clid") # client id
    tdh = request.GET.get("tdh") # tilda hook id
    context = {}
    if request.method == "POST":
        form = LidForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('lid_code'):
                form_name = form.cleaned_data['form_name']
                form_name = form_name.replace('+'," ")
                form.cleaned_data['form_name'] = form_name
            form.save()
            return redirect('crm:lids')
        else:
            print(form.errors)
    else:
        # form = LidForm(initial={'event_id': initial_event})
        context["form"] = LidForm()
        if tdh:
            context["tdh"] = WebHook.objects.filter(id=int(tdh)).first()
            body_s = context["tdh"].body
            body = json.loads(body_s)
            formid = body.get('formid')
            if formid == 'form472406355':
                form = LidForm(initial={'event_id': 51,
                                        'action': "Регистрация на сайте",
                                        'target': "Оплатить онлайн-марафон и зайти в канал"})
            context.update(body)
    return render(request, "crm/add_lid.html", context)

@login_required
def get_tilda(request):
    
    tildahooks = WebHook.objects.extra(
        tables=['lid'],
        where = [
            'crm_webhook.tranid=lid.lid_code',
        ]
    )[:1000].values()
    tildahooks_id = [pk['id'] for pk in tildahooks]
    
    qs = WebHook.objects.exclude(pk__in=tildahooks_id)
    pprint(qs)
    
    context = {
        "tildahooks": qs.order_by('-cdate')[:100]
    }
    return render(request, "crm/tilda_hooks.html", context)

@login_required
def list_detail(request, pk):
    
    if request.method == "POST":
        print('clients' in request.POST)
        if 'clients' in request.POST:
            form = AddClientsForm(request.POST)
            if form.is_valid():
                pl = PreviousList.objects.get(pk=pk)
                clients = form.cleaned_data['clients'].split(',')
                for cl in clients:
                    if cl and cl.isdigit():
                        try:
                            client = Client.objects.get(pk=cl)
                            pcl, created = PreviousListClient.objects.get_or_create(prev_list=pl,
                                                                                    client=client)
                            if created:
                                pcl.cuser = request.user
                                pcl.save()
                                
                        except Exception as e:
                            print(e)
                            break
        elif 'filter' in request.POST:
            form = AddClientsSetForm(request.POST)
            if form.is_valid():
                db = form.cleaned_data['db']
                groups = tuple(db)
                filter = form.cleaned_data['filter']
                state = form.cleaned_data['state']
                states = [state['id'] for state in state.values()]
                print(groups, filter, states)
                pl = PreviousList.objects.get(pk=pk)
                
                # выбираем клиентов:
                qs = Client.objects.filter(group__in=groups).extra(
                select={'id': 'clients_client.id',
                    'phone': 'clients_client.phone',
                    'state_name': 'client_state.name',
                    'is_assisting': 'client_products.is_assisting',
                    'future_assisting': 'client_products.future_assisting',
                    'is_base_course': 'client_products.is_base_course',
                    'course_candidate': 'client_products.course_candidate',
                    'is_school_level_1': 'client_products.is_school_level_1',
                    'is_school_level_2': 'client_products.is_school_level_2',
                    'is_school_level_3': 'client_products.is_school_level_3',
                    'ter_gr': 'client_products.tg'},
            tables=['client_state', 'client_products'],
            where=['clients_client.state_id=client_state.id',
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
                
                print(qs.values())
        
                for client in qs.values():
                    # проверяем, что клиента ещё нет в этом списке:
                    cl = Client.objects.get(pk=client['id'])
                    pcl, created = PreviousListClient.objects.get_or_create(prev_list=pl,
                                                                   client=cl)
                    if created:
                        print("Только что создан")
                        pcl.cuser = request.user
                        pcl.save()
                    
        return redirect('crm:list_detail', pk=pk)

    clients = PreviousListClient.objects.filter(prev_list=pk).extra(
        select={'client_family': 'clients_client.family',
                'client_name': 'clients_client.name',
                'client_patr': 'clients_client.patr',
                'client_city': 'clients_client.city',
                'client_state': 'client_state.name'},
        tables=['client_state','clients_client', 'crm_previouslistclient'],
        where=['clients_client.state_id=client_state.id',
            'crm_previouslistclient.client_id=clients_client.id']
    ).order_by('client__family', 'client__name').values()
    
    context = {
        "list": get_object_or_404(PreviousList, pk=pk),
        "clients": clients,
        "form": AddClientsSetForm(),
        "client_form": AddClientsForm(),
    }
    return render(request, "crm/prev_list.html", context)

@login_required
@require_POST
def remove_from_list(request, pk):
    pcl = request.POST.get('pcl')
    client = PreviousListClient.objects.get(pk=pcl)
    client.delete()
    return redirect('crm:list_detail', pk=pk) 

@login_required
def add_action(request):
    plc = request.GET.get("plc")
    lid = request.GET.get("lid")
    if lid:
        lid_model = Lid.objects.get(pk=lid)
    else:
        lid_model = None
    next = request.GET.get("next")
    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.worker = request.user
            action.save()
            if lid_model:
                lid_model.worker = request.user
                lid_model.save()
            if plc:
                return redirect('crm:get_lists')
            else:
                return redirect('crm:lids')
    else:
        context = {
            "form": ActionForm(),
            "plc": plc,
            "lid": lid,
            "next": next
        }
    return render(request, "crm/add_action.html", context)


@login_required
def edit_action(request, pk):
    action = get_object_or_404(Action, pk=pk)
    if request.user != action.worker:
        return redirect('crm:active')
    plc = request.GET.get("plc")
    lid = request.GET.get("lid")
    if lid:
        lid_model = Lid.objects.get(pk=lid)
    else:
        lid_model = None
    next = request.META.get('HTTP_REFERER')
    
    if request.method == "POST":
        form = ActionForm(request.POST, instance=action)
        if form.is_valid():
            action = form.save(commit=False)
            action.worker = request.user
            action.save()
            if lid_model:
                lid_model.worker = request.user
                lid_model.save()
            else:
                return redirect(next)
    else:
        context = {
            "form": ActionForm(instance=action),
            "plc": plc,
            "lid": lid,
            "next": next
        }
    return render(request, "crm/edit_action.html", context)

@login_required
def complete(request):
    plc = request.GET.get("plc")
    
    lid = request.GET.get("lid")
    
    qs = Action.objects.filter(state=True)
    
    if lid:
        qs = qs.filter(lid=lid)
    if plc:
        qs = qs.filter(plc=plc)
   
    context = {
        "history": qs,
        "plc": plc,
        "lid": lid,
        "page": "complete"
    }
    return render(request, "crm/actions.html", context)

@login_required
def active(request):
    
    filter = request.GET.get("filter")
    
    plc = request.GET.get("plc")
    
    lid = request.GET.get("lid")
    
    qs = Action.objects.filter(state=False)
    
    if lid:
        qs = qs.filter(lid=lid)
    if plc:
        qs = qs.filter(plc=plc)
        Action.objects.filter(state=False)
   
    if filter:
        if filter == 'all':
            pass # TODO тут нужно продумать вообще фильтры
    else:
        qs = qs.filter(worker=request.user)
   
    context = {
        "history": qs,
        "plc": plc,
        "lid": lid,
        "page": "active"
    }
    return render(request, "crm/actions.html", context)

class PreviousListClientViewSet(viewsets.ModelViewSet):
    # Возможно стоит заменить на generics RetrieveUpdateDelAPIView
    queryset = PreviousListClient.objects.all()
    serializer_class = PreviousListClientSerializer
    
    def perform_create(self, serializer):
        serializer.save(cuser=self.request.user)

