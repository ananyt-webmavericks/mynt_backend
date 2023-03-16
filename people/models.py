from django.db import models

# Create your models here.

from company.models import Company

PEOPLE_CHOICES = (
    ("TEAM","TEAM"),
    ("INVESTOR","INVESTOR"),
    ("ADVISOR","ADVISOR")
)

class People(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_id = models.ForeignKey( Company, on_delete=models.CASCADE)
    type = models.CharField(choices=PEOPLE_CHOICES,max_length=10,default="TEAM")
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    facebook_link = models.TextField(null=True)
    instagram_link = models.TextField(null=True)
    linked_in_link = models.TextField(null=True)
    description = models.TextField(null=True)
    profile_image = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)