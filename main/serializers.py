from rest_framework import serializers
from .models import *

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['front', 'back', 'type', 'tags', 'is_active', 'is_priority', 'is_started',  'interval', 'interval_unit'] 
        
