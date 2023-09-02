from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
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

from .utils import get_current_season

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
    down_date = timezone.now() - timedelta(weeks=1)# end_date__gte
    season = get_current_season()
    context = {
        "unit": "schedule",
        "page": 'events',
        "form": EventPlanForm(),
        "users": User.objects.filter(is_active=True),
        "events": EventPlan.objects.filter(
            end_date__gte=down_date,
            season=season).order_by('start_date')
    }
    return render(request, "events/events.html", context)

@login_required
def upcoming_events(request):
    down_date = timezone.now() - timedelta(weeks=1)# end_date__gte
    update = timezone.now() + timedelta(weeks=14) # start_date__lte
    context = {
        "unit": "schedule",
        "page": 'upcoming',
        "form": EventPlanForm(),
        "users": User.objects.filter(is_active=True),
        "events": EventPlan.objects.filter(
            end_date__gte=down_date,
            start_date__lte=update).order_by('start_date')
    }
    return render(request, "events/events.html", context)

@login_required
def top_session(request):
    down_date = timezone.now() - timedelta(weeks=1)# end_date__gte
    update = timezone.now() + timedelta(weeks=53) # start_date__lte
    context = {
        "unit": "schedule",
        "page": 'top_session',
        "form": EventPlanForm(),
        "users": User.objects.filter(is_active=True),
        "events": EventPlan.objects.filter(
             ~Q(event__sort='inner'),
            end_date__gte=down_date,
            start_date__lte=update).order_by('start_date')
    }
    return render(request, "events/top_sessions.html", context)

@login_required
def create_or_edit_to_plan(request):
    if request.method == 'POST':
        form = EventPlanForm(request.POST)
        if form.is_valid():
            
            start_date = form.cleaned_data.get('start_date').date()
            start_time = form.cleaned_data.get('start_time').time()
            
            end_date = form.cleaned_data.get('end_date').date()
            end_time = form.cleaned_data.get('end_time').time()
            
            season = form.cleaned_data.get('season')
            place = form.cleaned_data.get('place')
            user = form.cleaned_data.get('user')
            site = form.cleaned_data.get('site')
            event = form.cleaned_data.get('event')
            is_period = form.cleaned_data.get('is_period')
            period = form.cleaned_data.get('period') if is_period else None
            
            eventplans = []
            
            while start_date <= end_date:
                
                # Создаем объект datetime с использованием часового пояса по умолчанию
                start_datetime = datetime.combine(start_date, start_time)
                end_datetime = datetime.combine(end_date, end_time)
            
                # Конвертируем время в часовой пояс по умолчанию
                start_datetime = timezone.make_aware(start_datetime)
                
                end_datetime = timezone.make_aware(end_datetime)

                # eventplan = form.save(commit=False)
                # eventplan.start_date = start_datetime
                # eventplan.end_date = end_datetime
                
                eventplan = EventPlan.objects.create(
                start_date=start_datetime,
                end_date=end_datetime,
                season=season,
                event=event,
                place=place,
                is_period=is_period,
                period=period,
                site=site
                )
                
                eventplan.user.set(user)  # Сохраняем связи ManyToMany
            
            
                # TODO обозначить конец, может быть как раз end date
                # TODO Придумать, как редактировать такие мероприятия
                
                if is_period:
                    period = form.cleaned_data.get('period')
                    start_date += timedelta(days=period)
                    daydelta = end_datetime - start_datetime
                    if daydelta.days < period:
                        break
                else:
                    # Если не периодическое, то выходим из цикла
                    break
            
            return redirect('events')
        else:
            print(form.errors)
    else:
        form = EventPlanForm()


    context = {
        "users": User.objects.filter(is_active=True),
        "form": form
    }
    return render(request, "events/plan.html", context)

@login_required
def create_or_edit_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            print("Valid")
            form.save()
            return redirect('events')
        else:
            print("form.is_valid()", form.is_valid())
    else:
        form = EventForm()

    context = {
        "form": form
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
    