from rest_framework import serializers
from .models import Documents

class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ["id","company_id","document_type","document_name","document_url","agreement_status","contract_id","created_at","updated_at"]