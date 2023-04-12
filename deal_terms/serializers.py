from rest_framework import serializers
from .models import DealTerms
from campaign.models import Campaign
from company.models import Company
from deal_type.serializers import DealTypeNameSerializer

class DealTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealTerms
        fields = ["id","campaign_id","security_type","discount","valuation_cap","min_subscription",
                  "target","end_date","created_at","updated_at"]


class DealtermCompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id","company_logo","company_name","product_description","traction_description",
                  "status","created_at","updated_at"]


class DealtermCampaignCompanySerializer(serializers.ModelSerializer):
    company_id = DealtermCompanySerializers(read_only=True)
    class Meta:
        model = Campaign
        fields = ["id","company_id","status","created_at","updated_at"]



class DealTermsRefrenceSerializer(serializers.ModelSerializer):
    campaign_id = DealtermCampaignCompanySerializer(read_only=True)
    security_type = DealTypeNameSerializer(read_only=True)
    class Meta:
        model = DealTerms
        fields = ["id","campaign_id","security_type","discount","valuation_cap","min_subscription",
                  "target","end_date","created_at","updated_at"]