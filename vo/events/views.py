from django.shortcuts import render
from rest_framework import viewsets, serializers, generics, pagination

from .serializers import EventSerializer
from .models import Event, EventPlan

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('name')
    serializer_class = EventSerializer
    pagination_class = pagination.LimitOffsetPagination

def get_plan(request):
    context = {
        "events": EventPlan.objects.all().order_by('start_date')
    }
    return render(request, "events/events.html", context)