from django.db import models

# Create your models here.

from campaign.models import Campaign

class Highlights(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign_id = models.ForeignKey(Campaign , on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    highlight_image = models.TextField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    