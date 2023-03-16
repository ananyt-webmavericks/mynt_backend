from django.db import models

from company.models import Company

# Create your models here.

class Press(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_id = models.ForeignKey( Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    link = models.TextField(null=True)
    description = models.TextField(null=True)
    banner = models.TextField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)