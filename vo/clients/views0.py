from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, serializers, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StateSerializer, ClientSerializer, ClientProductsSerializer, ClientMailingSerializer, ClientInterestSerializer, ClientExtraSerializer
from .models import State, Client, ClientProducts, ClientMailing, ClientInterest
from .paginations import CustomPagination


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all().order_by('name')
    serializer_class = StateSerializer

class ClientExtraView(generics.ListAPIView):
    serializer_class = ClientExtraSerializer
    # queryset = Client.objects.all().order_by('family', 'name')
    
    queryset = Client.objects.all().extra(
            select={'interest': 'client_interest.comment',
                    'viber_group': 'client_mailing.viber_group',
                    'tg_group': 'client_mailing.tg_group',
                    'wa_group': 'client_mailing.wa_group',
                    'viber': 'client_mailing.viber',
                    'tg': 'client_mailing.tg',
                    'wa': 'client_mailing.wa',
                    'sms': 'client_mailing.sms',
                    'call': 'client_mailing.call',
                    'mailing': 'client_mailing.comment'},
            tables=['client_interest','client_mailing'],
            where=['clients_client.id=client_interest.client_id',
                'clients_client.id=client_mailing.client_id']
            ).order_by('family','name')
    
    pagination_class = CustomPagination  
    
    

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('family', 'name')
    serializer_class = ClientSerializer
    
    @action(methods=['get'],detail=False,
            url_path='extra2',url_name='extra2')
    def get_extra_info(self, request):
        queryset = Client.objects.all().extra(
            select={'interest': 'client_interest.comment',
                    'viber_group': 'client_mailing.viber_group',
                    'tg_group': 'client_mailing.tg_group',
                    'wa_group': 'client_mailing.wa_group',
                    'viber': 'client_mailing.viber',
                    'tg': 'client_mailing.tg',
                    'wa': 'client_mailing.wa',
                    'sms': 'client_mailing.sms',
                    'call': 'client_mailing.call',
                    'mailing': 'client_mailing.comment'},
            tables=['client_interest','client_mailing'],
            where=['clients_client.id=client_interest.client_id',
                'clients_client.id=client_mailing.client_id']
            ).order_by('family','name').values()
        pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ClientExtraSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ClientExtraSerializer(queryset, many=True)
        return Response(serializer.data)
    
class ClientProductsViewSet(viewsets.ModelViewSet):
    queryset = ClientProducts.objects.all()
    serializer_class = ClientProductsSerializer
    lookup_field = 'client_id'
    
    def retrieve(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id', None)
        self.queryset = ClientProducts.objects.filter(client_id=client_id)
        return super(ClientProductsViewSet, self).retrieve(request, *args, **kwargs)
    
class ClientMailingViewSet(viewsets.ModelViewSet):
    queryset = ClientMailing.objects.all()
    serializer_class = ClientMailingSerializer
    lookup_field = 'client_id'
    permission_classes= (IsAuthenticated,)
    
    def list(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id', None)
        self.queryset = ClientMailing.objects.filter(client_id=client_id)
        return super(ClientMailingViewSet, self).retrieve(request, *args, **kwargs)
    
class ClientInterestViewSet(viewsets.ModelViewSet):
    queryset = ClientInterest.objects.all()
    serializer_class = ClientInterestSerializer
    
    lookup_field = 'client_id'
    
    @action(methods=['get'], detail=False,
            url_path='products/(?P<client_id>[^/.]+)',
            url_name='products')
    def  get_products(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id', None)
        print(client_id)
        queryset = ClientInterest.objects.filter(client_id=client_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ClientInterestSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ClientInterestSerializer(queryset, many=True)
        return Response(serializer.data)