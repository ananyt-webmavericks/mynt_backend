from django.db import models

# Create your models here.

from company.models import Company

DOCUMENT_CHOICES = (
    ("AGREEMENTS","AGREEMENTS"),
    ("DOCUMENTS","DOCUMENTS")
)

AGREEMENT_STATUS_CHOICES = (
    ("UPLOADED BY ADMIN","UPLOADED BY ADMIN"),
    ("SIGNED BY FOUNDER","SIGNED BY FOUNDER"),
    ("SIGNED BY ADMIN","SIGNED BY ADMIN")
)

class Documents(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_id = models.ForeignKey( Company, on_delete=models.CASCADE)
    document_type = models.CharField(choices=DOCUMENT_CHOICES,max_length=12,default="DOCUMENTS")
    document_name = models.CharField(max_length=100)
    agreement_status = models.CharField(choices=AGREEMENT_STATUS_CHOICES , max_length=200, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)