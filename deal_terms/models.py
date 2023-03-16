from django.db import models

# Create your models here.

from campaign.models import Campaign

DEAL_TYPE = (
    ("CSOP","CSOP"),
    ("CCD","CCD"),
    ("NCD","NCD"),
    ("ID","ID")
)

class DealTerms(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign_id = models.ForeignKey(Campaign , on_delete=models.CASCADE)
    security_type = models.CharField(choices=DEAL_TYPE,max_length=20,default="CSOP")
    discount = models.CharField(max_length=2)
    valuation_cap = models.CharField(max_length=12)
    min_subscription = models.CharField(max_length=12)
    target = models.CharField(max_length=12)
    end_date = models.DateField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)