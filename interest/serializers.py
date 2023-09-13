from rest_framework import serializers
from .models import Interest
class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ["id","investor_id","campaign_id","company_name","investor_first_name","investor_last_name","investor_email","investor_mobile_number","applied_date","created_at","updated_at"]