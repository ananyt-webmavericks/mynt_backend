
from rest_framework import serializers
from .models import CampaignDocument

class CampaignDocumentSerializers(serializers.ModelSerializer):
    class Meta:
        model = CampaignDocument
        fields = ["id","user_id","agreement_status","agreement_url","agreement_name","campaign_id","created_at","updated_at"]