from rest_framework import serializers
from .models import Payment
from campaign.models import Campaign
from company.models import Company
from documents.serializers import DocumentsSerializer

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id","campaign_id","user_id","cashfree_order_id","mynt_order_id","amount","total_amount","status","payment_mode","payment_session_id","transaction_id","created_at","updated_at"]


class InvestorCompanySerializers(serializers.ModelSerializer):
    documents = DocumentsSerializer(source='documents_set', many=True, read_only=True)
    class Meta:
        model = Company
        fields = ["id","company_logo","company_name","status","created_at",
                    "updated_at","documents"]

class InvestorCampaignSerializer(serializers.ModelSerializer):
    company_id = InvestorCompanySerializers(read_only=True)
    class Meta:
        model = Campaign
        fields = ["id","company_id","status","created_at","updated_at"]

class InvestorPaymentSerializer(serializers.ModelSerializer):
    campaign_id = InvestorCampaignSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = ["id","campaign_id","user_id","cashfree_order_id","mynt_order_id","amount","total_amount","status","payment_mode","payment_session_id","transaction_id","created_at","updated_at"]
