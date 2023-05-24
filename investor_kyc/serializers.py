from rest_framework import serializers
from .models import InvestorKyc

class InvestorKycSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorKyc
        fields = ["id",
                    "user_id",
                    "pan_card",
                    "pan_card_verified",
                    "birth_date",
                    "birth_month",
                    "birth_year",
                    "address_line_1",
                    "address_line_2",
                    "city",
                    "state",
                    "country",
                    "pincode",
                    "bank_name",
                    "bank_account",
                    "ifsc_code",
                    "bank_account_verified",
                    "linkedin_profile",
                    "mobile_number",
                    "mobile_number_otp",
                    "mobile_number_verified",
                    "aadhaar_card_number",
                    "aadhaar_card_verified",
                    "created_at",
                    "updated_at"]