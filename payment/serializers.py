from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id","campaign_id","user_id","cashfree_order_id","mynt_order_id","amount","status","payment_session_id","created_at","updated_at"]