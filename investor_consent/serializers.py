from rest_framework import serializers
from .models import InvestorConsent
class InvestorConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorConsent
        fields = ["id","user_id","risk_consent","limited_transfer_consent","diversification_consent","cancellation_consent","research_consent","created_at","updated_at"]