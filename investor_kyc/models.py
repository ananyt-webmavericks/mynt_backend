from django.db import models

# Create your models here.
from mynt_users.models import MyntUsers

class InvestorKyc(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(MyntUsers , on_delete=models.CASCADE)
    pan_card = models.CharField(max_length=11 , null=True)
    pan_card_verified = models.BooleanField(default=False)
    birth_date = models.CharField(max_length=3,null=True)
    birth_month = models.CharField(max_length=3,null=True)
    birth_year = models.CharField(max_length=5, null=True)
    address_line_1 = models.CharField(max_length=100,null=True)
    address_line_2 = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=50 , null=True)
    country = models.CharField(max_length=50,default='India')
    pincode = models.CharField(max_length=10,null=True)
    bank_name = models.CharField(max_length=100 , null=True)
    bank_account = models.CharField(max_length=50 , null=True)
    ifsc_code = models.CharField(max_length=50,null=True)
    bank_account_verified = models.BooleanField(default=False)
    linkedin_profile = models.TextField(null=True)
    mobile_number = models.CharField(max_length=20,null=True)
    mobile_number_otp = models.CharField(max_length=6,default=None , null=True)
    mobile_number_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)