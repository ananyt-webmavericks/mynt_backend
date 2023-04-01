from django.db import models

# Create your models here.

PAYMENT_STATUSES = (
    ("PENDING","PENDING"),
    ("COMPLETED","COMPLETED"),
    ("FAILED","FAILED")
)

from campaign.models import Campaign
from mynt_users.models import MyntUsers

class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign_id = models.ForeignKey(Campaign , on_delete=models.CASCADE)
    user_id = models.ForeignKey(MyntUsers , on_delete=models.CASCADE)
    cashfree_order_id = models.CharField(max_length=20 , null=True)
    mynt_order_id = models.CharField(max_length=40 , null=True)
    amount = models.CharField(max_length=5,null=True)
    status = models.CharField(choices=PAYMENT_STATUSES,max_length=10,default="PENDING")
    payment_session_id = models.TextField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)