from rest_framework import serializers
from .models import DealTerms

class DealTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealTerms
        fields = ["id","campaign_id","security_type","discount","valuation_cap","min_subscription",
                  "target","end_date","created_at","updated_at"]