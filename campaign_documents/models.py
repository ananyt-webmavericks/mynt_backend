from django.db import models

from campaign.models import Campaign
from company.models import Company
from mynt_users.models import MyntUsers


STATUS = (
    ("UPLOADED BY FOUNDER","UPLOADED BY FOUNDER"),
    ("SIGNED BY INVESTOR","SIGNED BY INVESTOR"),
    ("SIGNED BY FOUNDER","SIGNED BY FOUNDER"),
)

# Create your models here.

class CampaignDocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign_id = models.ForeignKey( Campaign, on_delete=models.CASCADE)
    user_id = models.ForeignKey( MyntUsers, on_delete=models.CASCADE)
    agreement_status = models.CharField(choices=STATUS , max_length=200, null=True)
    agreement_url = models.TextField(null=True)
    agreement_name = models.TextField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)