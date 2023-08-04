from rest_framework import serializers

from .models.previous_list_client import  PreviousListClient

class PreviousListClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousListClient
        fields = ('prev_list', 'client_id', 'cdate', 'cuser')
        read_only_fields = ('cdate', 'cuser')