from rest_framework import serializers
from .models import Faqs

class FaqsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        fields = ["id","campaign_id","question","answer","created_at","updated_at"]