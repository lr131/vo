from django.shortcuts import render
from rest_framework import viewsets, serializers, generics, pagination

from .serializers import EventSerializer
from .models import Event

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('name')
    serializer_class = EventSerializer
    pagination_class = pagination.LimitOffsetPagination
