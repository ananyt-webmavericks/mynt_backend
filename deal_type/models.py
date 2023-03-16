from django.db import models

# Create your models here.

class DealType(models.Model):
    id = models.BigAutoField(primary_key=True)
    deal_name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)