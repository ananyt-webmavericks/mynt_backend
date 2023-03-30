from django.db import models

# Create your models here.

from campaign.models import Campaign

class Rewards(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign_id = models.ForeignKey(Campaign , on_delete=models.CASCADE)
    amount = models.CharField(max_length=12)
    product_name = models.CharField(max_length=100)
    discounted_price = models.IntegerField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)