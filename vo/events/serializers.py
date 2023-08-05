from rest_framework import serializers

from .models.place import Place
from .models.event_state import EventState
from .models.event import Event
from .models.event_plan import EventPlan
from .models.event_type import EventType


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        
class EventPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPlan
        fields = '__all__'
        

class EventPlanExtraSerializer(serializers.Serializer):
    """Сериализатор для представления 
    данных клиента в общем виде в апи, только чтение!"""
    id = serializers.IntegerField()
    start_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False, read_only=True)
    end_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False, read_only=True)
    event_id = serializers.IntegerField() # что
    place_id = serializers.IntegerField() # где
    is_period = serializers.BooleanField(default=False)
    period = serializers.IntegerField()
    
    event_name = serializers.CharField()
    event_type = serializers.CharField()
    place_name = serializers.CharField()