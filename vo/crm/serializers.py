from rest_framework import serializers

from .models import  PreviousListClient

class PreviousListClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousListClient
        fields = ('prev_list', 'client_id', 'cdate', 'cuser')
        read_only_fields = ('cdate', 'cuser')