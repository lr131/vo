from rest_framework.views import APIView
from rest_framework import viewsets, serializers, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from users.views import client

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
    
    
class ClientExtraView(generics.ListAPIView):
    # pagination_class = CustomPagination
    serializer_class = ClientExtraSerializer
    
    # queryset = Client.objects.all().extra(
    #         select={'interest': 'client_interest.comment',
    #                 'viber_group': 'client_mailing.viber_group',
    #                 'tg_group': 'client_mailing.tg_group',
    #                 'wa_group': 'client_mailing.wa_group',
    #                 'viber': 'client_mailing.viber',
    #                 'tg': 'client_mailing.tg',
    #                 'wa': 'client_mailing.wa',
    #                 'sms': 'client_mailing.sms',
    #                 'call': 'client_mailing.call',
    #                 'mailing': 'client_mailing.comment'},
    #         tables=['client_interest','client_mailing'],
    #         where=['clients_client.id=client_interest.client_id',
    #             'clients_client.id=client_mailing.client_id']
    #         ).order_by('family','name').values()
    
    def get_queryset(self):
        user = self.request.user
        groups = list(map(lambda x: x['name'],user.groups.all().values()))
        print(groups)
        return Client.objects.filter(group__in=groups).extra(
            select={'state_name': 'client_state.name',
                    'viber_group': 'client_mailing.viber_group',
                    'tg_group': 'client_mailing.tg_group',
                    'wa_group': 'client_mailing.wa_group',
                    'viber': 'client_mailing.viber',
                    'tg': 'client_mailing.tg',
                    'wa': 'client_mailing.wa',
                    'sms': 'client_mailing.sms',
                    'call': 'client_mailing.call',
                    'mailing': 'client_mailing.comment'},
            tables=['client_state','client_mailing'],
            where=['clients_client.state_id=client_state.id',
                'clients_client.id=client_mailing.client_id']
            ).order_by('family','name').values()
    
    # def list(self, request):
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = ClientExtraSerializer(queryset, many=True)
    #     return Response(serializer.data)


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
