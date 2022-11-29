from django.shortcuts import render
from rest_framework import viewsets, serializers, generics, pagination, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import EventSerializer, EventPlanSerializer, EventPlanExtraSerializer
from .models import Event, EventPlan

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('name')
    serializer_class = EventSerializer
    pagination_class = pagination.LimitOffsetPagination
    
class EventPlanViewSet(viewsets.ModelViewSet):
    queryset = EventPlan.objects.all().order_by('start_date')
    serializer_class = EventPlanSerializer
    pagination_class = pagination.LimitOffsetPagination
    

def get_plan(request):
    context = {
        "events": EventPlan.objects.all().order_by('start_date')
    }
    return render(request, "events/events.html", context)

class EventPlanExtraView(generics.ListAPIView):
    serializer_class = EventPlanExtraSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    def get_queryset(self):
        # TODO ищёт только по имени тренинга!
        search = self.request.query_params.get('search', None)
        param = f"%{search}%"
        if search:
            qs = EventPlan.objects.all().extra(
            select={
                'event_name': 'events_event.name',
                'event_type': 'event_types.name',
                'place_name': 'events_place.addr',
            },
            tables = ['events_event', 'event_types', 'events_place'],
            where=['event_plan.event_id=events_event.id', 
                   'events_event.event_type_id=event_types.id',
                   'event_plan.place_id=events_place.id',
                   'events_event.name LIKE %s'],
            params=[param]
            ).order_by('start_date')
        else:
            
            qs = EventPlan.objects.all().extra(
                select={
                    'event_name': 'events_event.name',
                    'event_type': 'event_types.name',
                    'place_name': 'events_place.addr',
                },
                tables = ['events_event', 'event_types', 'events_place'],
                where=['event_plan.event_id=events_event.id', 
                    'events_event.event_type_id=event_types.id',
                    'event_plan.place_id=events_place.id']
            ).order_by('start_date')
        
        return qs.values()
    