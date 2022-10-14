from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import State, Client, ClientProducts, ClientMailing, ClientInterest

class StateSerializer(serializers.ModelSerializer):
    """Класс-сериализатор статусов клиента"""
    ##TODO здесь доступны и создание, и удаление, и обновление!
    class Meta:
        model = State
        fields = ('id', 'name', 'description')
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        
class ClientExtraSerializer(serializers.Serializer):
    """Сериализатор для представления 
    данных клиента в общей таблице"""
    id = serializers.IntegerField()
    family = serializers.CharField(max_length=250)
    name = serializers.CharField(max_length=250)
    patr = serializers.CharField(max_length=250)
    birthday = serializers.CharField()
    city = serializers.CharField(max_length=250)
    phone = serializers.CharField(max_length=250)
    in_black_list = serializers.BooleanField(default=False)
    state_id = serializers.IntegerField()
    comment = serializers.CharField()
    note = serializers.CharField()
    group = serializers.CharField(max_length=10)

    viber_group = serializers.BooleanField(default=False)
    tg_group = serializers.BooleanField(default=False)
    wa_group = serializers.BooleanField(default=False)
    viber = serializers.BooleanField(default=False)
    tg = serializers.BooleanField(default=False)
    wa = serializers.BooleanField(default=False)
    sms = serializers.BooleanField(default=False)
    call = serializers.BooleanField(default=False)
    mailing = serializers.CharField(default=False)
    
    state_name = serializers.CharField()   
        
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProducts
        fields = ('id','client', 'is_assisting', 'future_assisting',
                  'is_base_course', 'course_candidate', 'is_school_level_1',
                  'is_school_level_2', 'is_school_level_3', 'tg')
        
class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMailing
        fields = ('id','client', 'viber_group', 'wa_group', 'tg_group',
                  'tg', 'wa', 'viber', 'sms', 'call', 'comment')
        
class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientInterest
        fields = ('id', 'client', 'event', 'comment')