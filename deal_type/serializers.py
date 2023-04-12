from rest_framework import serializers
from .models import DealType

class DealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealType
        fields = ["id", "deal_name", "created_at", "updated_at"]
        

class DealTypeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealType
        fields = ["id", "deal_name"]
