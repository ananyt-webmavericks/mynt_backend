
from rest_framework import serializers
from .models import Company

class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id","user_id","company_logo","founder_linked_in_profile","company_name","company_linked_in_profile","website_url","previous_funding",
                  "product_description","traction_description","revenue","reason_for_community_round","reason_for_mynt","existing_commitments","company_pitch",
                    "country","state","city","pincode","company_address","facebook_link","instagram_link","legal_name","cin","date_of_incorporation",
                    "incorporation_type","sector","invested_so_far","number_of_employees","status","created_at",
                    "updated_at"]