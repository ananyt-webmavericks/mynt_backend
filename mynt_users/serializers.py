from rest_framework import serializers
from .models import MyntUsers
class MyntUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyntUsers
        fields = ["id","first_name","last_name","email","email_otp","social_login","country","email_verified","nationality","created_at","updated_at","profile_image","user_type"]