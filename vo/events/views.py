from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import viewsets, serializers, generics, pagination, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from .serializers import EventSerializer, EventPlanSerializer, EventPlanExtraSerializer

from .models.event import Event
from .models.event_plan import EventPlan

from .forms import EventForm, EventPlanForm

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('name')
    serializer_class = EventSerializer
    pagination_class = pagination.LimitOffsetPagination
    
class EventPlanViewSet(viewsets.ModelViewSet):
    queryset = EventPlan.objects.all().order_by('start_date')
    serializer_class = EventPlanSerializer
    pagination_class = pagination.LimitOffsetPagination
    
@login_required
def get_plan(request):
    down_date = timezone.now() - timedelta(weeks=5)# end_date__gte
    update = timezone.now() + timedelta(weeks=14) # start_date__lte
    context = {
        "form": EventPlanForm(),
        "users": User.objects.filter(is_active=True),
        "events": EventPlan.objects.filter(
            end_date__gte=down_date,
            start_date__lte=update).order_by('-start_date')
    }
    return render(request, "events/events.html", context)


@login_required
def create_or_edit_to_plan(request):
    down_date = timezone.now() - timedelta(weeks=5)# end_date__gte
    update = timezone.now() + timedelta(weeks=14) # start_date__lte
    context = {
        "form": EventPlanForm()
    }
    return render(request, "events/event.html", context)

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
    