from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework import viewsets, serializers, generics, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import State, Client, ClientProducts, ClientMailing, ClientInterest
from .serializers import ClientExtraSerializer, StateSerializer, ProductsSerializer, MailingSerializer, InterestSerializer, ClientSerializer
from .paginations import CustomPagination

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all().order_by('name')
    serializer_class = StateSerializer
    

class ClientViewSet(viewsets.ModelViewSet):
    # Возможно стоит заменить на generics RetrieveUpdateDelAPIView
    queryset = Client.objects.all().order_by('family', 'name')
    serializer_class = ClientSerializer
    
    def perform_create(self, serializer):
        serializer.save(cuser=self.request.user, 
                        muser=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(muser=self.request.user)
    
    
class ClientExtraView(generics.ListAPIView):
    # pagination_class = CustomPagination
    serializer_class = ClientExtraSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['state__name', 'city', 'group', 'have_kids']
    search_fields = ['family', 'name', 'phone']
    
    def get_queryset(self):
        user = self.request.user
        groups = list(map(lambda x: x['name'],user.groups.all().values()))
        filter = self.request.query_params.get('filter', None)
        
        qs = Client.objects.filter(group__in=groups).extra(
            select={'state_name': 'client_state.name',
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
            print("filter", filter)
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
        return qs.values()


class ClientProductsView(generics.RetrieveAPIView):
    queryset = ClientProducts.objects.all()
    serializer_class = ProductsSerializer
    lookup_field = 'client_id'


class ClientMailingView(generics.RetrieveAPIView):
    queryset = ClientMailing.objects.all()
    serializer_class = MailingSerializer
    lookup_field = 'client_id'    
    
# class ProductsViewSet(viewsets.ModelViewSet):
class ProductsViewSet(viewsets.ModelViewSet):
    queryset = ClientProducts.objects.all()
    serializer_class = ProductsSerializer
    
class MailingViewSet(viewsets.ModelViewSet):
    queryset = ClientMailing.objects.all()
    serializer_class = MailingSerializer
    
class InterestViewSet(viewsets.ModelViewSet):
    queryset = ClientInterest.objects.all()
    serializer_class = InterestSerializer
    
class ClientInterestView(generics.ListCreateAPIView):
    """Класс, показывающий, какими продуктами интересовался конкртеный клиент"""
    serializer_class = InterestSerializer
        
    def get_queryset(self):
        client_id = self.kwargs.get('client_id', None)
        return ClientInterest.objects.filter(client_id=client_id)
    
class ProductInterestView(generics.ListAPIView):
    """Класс, показывающий, какие клиенты интересовались конкретным продуктом"""
    serializer_class = InterestSerializer
    
    def get_queryset(self):
        event = self.kwargs.get('event_id', None)
        return ClientInterest.objects.filter(event=event)

@login_required
def client(request, pk):
    context = {
        'user': request.user,
        'pk': pk,
        'back_page': request.GET.get("back_page", 1),
        'states': State.objects.all().order_by('name')
    } 
    return render(request, 'clients/client.html', context=context)

@login_required
def create_client(request):
    context = {
        'user': request.user,
        'back_page': request.GET.get("back_page", 1),
        'states': State.objects.all().order_by('name')
    } 
    return render(request, 'clients/new_client.html', context=context)

@login_required
def clients(request):
    context = {
        'user': request.user,
        'page': request.GET.get("page", 1)
    }
    return render(request, 'clients/clients_list.html', context=context)

