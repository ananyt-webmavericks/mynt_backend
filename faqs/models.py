from django.db import models

# Create your models here.

from campaign.models import Campaign

class Faqs(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign_id = models.ForeignKey(Campaign , on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)