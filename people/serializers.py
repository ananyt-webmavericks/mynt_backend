from rest_framework import serializers
from .models import People

class Peopleserializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ["id","company_id","type","name","position","facebook_link","instagram_link","linked_in_link","description","profile_image","created_at","updated_at"]