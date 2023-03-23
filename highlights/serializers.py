from rest_framework import serializers
from .models import Highlights

class Highlightsserializer(serializers.ModelSerializer):
    class Meta:
        model = Highlights
        fields = ["id","campaign_id","title","description","highlight_image","created_at","updated_at"]