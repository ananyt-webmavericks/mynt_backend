from rest_framework import serializers
from company.serializers import CompanySerializers
from .models import Campaign

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["id","company_id","status","youtube_link","ama_date","ama_meet_link","ama_youtube_video","pitch","created_at","updated_at"]


class CampaignSerializerWithCompanySerializer(serializers.ModelSerializer):
    company_id = CompanySerializers(many=False, read_only=True)
    class Meta:
        model = Campaign
        fields = ["id","company_id","status","youtube_link","ama_date","ama_meet_link","ama_youtube_video","pitch","created_at","updated_at"]
