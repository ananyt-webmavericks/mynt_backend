from rest_framework import serializers
from .models import Press
import ast

class Pressserializer(serializers.ModelSerializer):
    banner_images = serializers.SerializerMethodField()
    class Meta:
        model = Press
        fields = ["id","company_id","title","link","description","banner","banner_images","created_at","updated_at"]
        optional_fields = ["banner_images"]

    def get_banner_images(self, obj):
        res = ast.literal_eval(obj.banner)
        return res