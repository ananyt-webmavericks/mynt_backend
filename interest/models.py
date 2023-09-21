from django.db import models
from mynt_users.models import MyntUsers
from campaign.models import Campaign

# Create your models here.

class Interest(models.Model):
    id = models.BigAutoField(primary_key=True)
    investor_id = models.ForeignKey(MyntUsers , on_delete=models.CASCADE)
    campaign_id = models.ForeignKey(Campaign , on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100 , null=True)
    investor_first_name = models.CharField(max_length=60,null=True)
    investor_last_name = models.CharField(max_length=60,null=True)
    investor_email = models.CharField(max_length=100,null=True)
    investor_mobile_number = models.CharField(max_length=20,null=True)
    applied_date = models.DateTimeField()
    amount = models.CharField(max_length=10,default=0)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)