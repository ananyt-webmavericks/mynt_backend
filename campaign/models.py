from django.db import models

# Create your models here.

from company.models import Company

CAMPAIGN_STATUS = (
    ("CREATED","CREATED"),
    ("UNDER REVIEW","UNDER REVIEW"),
    ("CHANGES REQUESTED","CHANGES REQUESTED"),
    ("APPROVED","APPROVED"),
    ("LIVE","LIVE"),
    ("COMPLETED","COMPLETED"),
    ("REFUNDED","REFUNDED"),
    ("CLOSED","CLOSED")
)

class Campaign(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_id = models.ForeignKey( Company, on_delete=models.CASCADE)
    status = models.CharField(choices=CAMPAIGN_STATUS,max_length=100,default="CREATED")
    youtube_link = models.TextField(null=True)
    ama_date = models.DateField(null=True)
    ama_meet_link = models.TextField(null=True)
    ama_youtube_video = models.TextField(null=True)
    pitch = models.TextField(null=True)
    total_investors = models.CharField(max_length=10,null=True)
    total_raised = models.CharField(max_length=10,null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
