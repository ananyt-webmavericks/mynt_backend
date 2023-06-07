from rest_framework import serializers
from .models import Press
import ast

class Pressserializer(serializers.ModelSerializer):
    banner_images = serializers.SerializerMethodField('get_banner_images')
    class Meta:
        model = Press
        fields = ["id","company_id","title","link","description","banner","banner_images","created_at","updated_at"]

    def get_banner_images(self, obj):
        if not obj.banner:
            obj.banner = []

        if isinstance(obj.banner, list):
            return obj.banner
        
        if "[" in obj.banner:
            res = ast.literal_eval(obj.banner)
            return res
        return obj.banner