from rest_framework import serializers
from .models import Press

class Pressserializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ["id","company_id","title","link","description","banner","created_at","updated_at"]