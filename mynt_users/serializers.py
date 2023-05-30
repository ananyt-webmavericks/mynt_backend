from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import MyntUsers
class MyntUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyntUsers
        fields = ["id","first_name","last_name","email","email_otp","password","secondary_email","secondary_email_otp","secondary_email_verified","social_login","country","email_verified","nationality","created_at","updated_at","profile_image","user_type"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
       # The default result (access/refresh tokens)
       data = super().validate(attrs)
       refresh = self.get_token(self.user)

       # assign token 
       data['refresh'] = str(refresh)
       data['access'] = str(refresh.access_token)

       # extra fields
    #    data['age'] = self.user.age
       return data        