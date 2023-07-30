from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, serializers, generics, filters
from pprint import pprint
from .forms import ClientEventHistoryForm, PreviousListForm, ActionForm, LidForm
from .models import Action, ClientEventHistory, PreviousList, PreviousListClient
from .models import WebHook, Lid
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
        if form.is_valid():
            prev_list = form.save(commit=False)
            prev_list.cuser = request.user
            # prev_list.date = timezone.now()
            prev_list.save()
            return redirect('crm:get_lists')
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
    context = {
        "lids": Lid.objects.filter(worker__isnull=True).order_by('-date')[:100]
    }
    # TODO фильтровать по воркерам, выводить те, что без них
    return render(request, "crm/lids.html", context)

@login_required
def add_lid(request):
    clid = request.GET.get("clid") # client id
    tdh = request.GET.get("tdh") # tilda hook id
    context = {}
    if request.method == "POST":
        form = LidForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print(form)
            form.save()
            return redirect('crm:lids')
        else:
            print(form.errors)
    else:
        context["form"] = LidForm()
        if tdh:
            print('tdh',tdh)
            context["tdh"] = WebHook.objects.filter(id=int(tdh)).first()
            body_s = context["tdh"].body
            body = json.loads(body_s)
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
    
    clients = PreviousListClient.objects.filter(prev_list=pk).extra(
        select={'client_family': 'clients_client.family',
                'client_name': 'clients_client.name',
                'client_patr': 'clients_client.patr',
                'client_city': 'clients_client.city',
                'client_state': 'client_state.name'},
        tables=['client_state','clients_client', 'crm_previouslistclient'],
        where=['clients_client.state_id=client_state.id',
            'crm_previouslistclient.client_id=clients_client.id']
    ).values()
    
    context = {
        "list": get_object_or_404(PreviousList, pk=pk),
        "clients": clients
    }
    return render(request, "crm/prev_list.html", context)

@login_required
def add_action(request):
    plc = request.GET.get("plc")
    lid = request.GET.get("lid")
    next = request.GET.get("next")
    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.worker = request.user
            action.save()
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
        "page": "history"
    }
    return render(request, "crm/actions.html", context)

@login_required
def active(request):
    plc = request.GET.get("plc")
    
    lid = request.GET.get("lid")
    
    qs = Action.objects.filter(state=False)
    
    if lid:
        qs = qs.filter(lid=lid)
    if plc:
        qs = qs.filter(plc=plc)
   
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

