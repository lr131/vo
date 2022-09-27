from rest_framework import serializers
from .models import State, Client, ClientProducts, ClientMailing, ClientInterest

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        
class ClientExtraSerializer(serializers.Serializer):
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

    viber_group = serializers.BooleanField(default=False)
    tg_group = serializers.BooleanField(default=False)
    wa_group = serializers.BooleanField(default=False)
    viber = serializers.BooleanField(default=False)
    tg = serializers.BooleanField(default=False)
    wa = serializers.BooleanField(default=False)
    sms = serializers.BooleanField(default=False)
    call = serializers.BooleanField(default=False)
    mailing = serializers.CharField(default=False)
    
    interest = serializers.CharField()   
        
class ClientProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProducts
        fields = '__all__'
        
class ClientMailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMailing
        fields = '__all__'
        
class ClientInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientInterest
        fields = '__all__'