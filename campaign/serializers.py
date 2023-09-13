from rest_framework import serializers
from faqs.serializers import FaqsSerializers
from rewards.serializers import Rewardsserializer
from documents.serializers import DocumentsSerializer
from people.serializers import Peopleserializer
from highlights.serializers import Highlightsserializer
from press.serializers import Pressserializer
from .models import Campaign
from company.models import Company

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["id","company_id","status","youtube_link","ama_date","ama_meet_link","ama_youtube_video","pitch","total_investors","total_raised","created_at","updated_at"]


class CompanyRefrencesSerializers(serializers.ModelSerializer):
    documents = DocumentsSerializer(source='documents_set', many=True, read_only=True)
    peoples = Peopleserializer(source='people_set', many=True, read_only=True)
    press = Pressserializer(source='press_set', many=True, read_only=True)
    class Meta:
        model = Company
        fields = ["id","user_id","company_logo","founder_linked_in_profile","company_name","company_linked_in_profile","website_url","previous_funding",
                  "product_description","traction_description","revenue","reason_for_community_round","reason_for_mynt","existing_commitments","company_pitch",
                    "country","state","city","pincode","company_address","facebook_link","instagram_link","legal_name","cin","date_of_incorporation",
                    "incorporation_type","sector","invested_so_far","number_of_employees","status","created_at",
                    "updated_at","documents","peoples","press"]


class CampaignSerializerWithCompanySerializer(serializers.ModelSerializer):
    company_id = CompanyRefrencesSerializers(read_only=True)
    faqs = FaqsSerializers(source='faqs_set', many=True, read_only=True)
    rewards = Rewardsserializer(source='rewards_set', many=True, read_only=True)
    higlights = Highlightsserializer(source='highlights_set', many=True, read_only=True)
    class Meta:
        model = Campaign
        fields = ["id","company_id","status","youtube_link","ama_date","ama_meet_link",
                  "ama_youtube_video","pitch","total_raised","total_investors","created_at","updated_at","faqs","rewards","higlights"]

