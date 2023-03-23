from rest_framework import serializers
from .models import Rewards

class Rewardsserializer(serializers.ModelSerializer):
    class Meta:
        model = Rewards
        fields = ["id","campaign_id","amount","product_name","description","created_at","updated_at"]