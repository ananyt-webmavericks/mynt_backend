from django.db import models

# Create your models here.

from campaign.models import Campaign
from deal_type.models import DealType



class DealTerms(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign_id = models.ForeignKey(Campaign , on_delete=models.CASCADE)
    security_type = models.ForeignKey(DealType, on_delete=models.CASCADE)
    discount = models.CharField(max_length=3)
    valuation_cap = models.CharField(max_length=12)
    min_subscription = models.CharField(max_length=12)
    target = models.CharField(max_length=12)
    end_date = models.DateField()
    enable_offline = models.BooleanField(default=False)
    bank_name = models.CharField(max_length=100 , null=True)
    account_no = models.CharField(max_length=50 , null=True)
    ifsc_code = models.CharField(max_length=50 , null=True)
    account_name = models.CharField(max_length=100 , null= True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)