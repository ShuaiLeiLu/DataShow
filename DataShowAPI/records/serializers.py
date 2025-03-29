from rest_framework import serializers
from .models import TradeRecord

class TradeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeRecord
        fields = '__all__'