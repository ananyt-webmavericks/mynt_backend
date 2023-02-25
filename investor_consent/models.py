from django.db import models
from mynt_users.models import MyntUsers

# Create your models here.

class InvestorConsent(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(MyntUsers , on_delete=models.CASCADE)
    risk_consent = models.BooleanField(default=False)
    limited_transfer_consent = models.BooleanField(default=False)
    diversification_consent = models.BooleanField(default=False)
    cancellation_consent = models.BooleanField(default=False)
    research_consent = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)