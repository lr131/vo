from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, serializers, generics, filters
from pprint import pprint
from .forms import ClientEventHistoryForm, PreviousListForm, ActionForm
from .models import Action, ClientEventHistory, PreviousList, PreviousListClient
from .serializers import PreviousListClientSerializer

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
            return redirect('crm:get_lists')
    else:
        context = {
            "form": ActionForm(),
            "plc": plc,
            "lid": lid,
            "next": next
        }
        pprint(context)
    return render(request, "crm/add_action.html", context)

@login_required
def history(request):
    plc = request.GET.get("plc")
    
    lid = request.GET.get("lid")
    
    qs = Action.objects.all()
    
    if lid:
        qs = qs.filter(lid=lid)
    if plc:
        qs = qs.filter(plc=plc)
   
    context = {
        "history": qs,
        "plc": plc,
        "lid": lid,
    }
    return render(request, "crm/history.html", context)

class PreviousListClientViewSet(viewsets.ModelViewSet):
    # Возможно стоит заменить на generics RetrieveUpdateDelAPIView
    queryset = PreviousListClient.objects.all()
    serializer_class = PreviousListClientSerializer
    
    def perform_create(self, serializer):
        serializer.save(cuser=self.request.user)

