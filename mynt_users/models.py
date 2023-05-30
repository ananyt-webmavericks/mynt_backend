from django.db import models

# Create your models here.

USER_CHOICES = (
    ("INVESTOR","INVESTOR"),
    ("FOUNDER","FOUNDER"),
    ("ADMIN","ADMIN")
)

class MyntUsers(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=100 , unique=True)
    email_otp = models.CharField(max_length=6,default=None , null=True)
    password = models.CharField(max_length=128,null=True)
    secondary_email = models.CharField(max_length=100 , default=None, null=True)
    secondary_email_otp = models.CharField(max_length=6,default=None , null=True)
    secondary_email_verified = models.BooleanField(default=False)
    social_login = models.BooleanField(default=False)
    country = models.CharField(max_length=100,default=None , null=True)
    nationality = models.CharField(max_length=100,default=None , null=True)
    email_verified = models.BooleanField(default=False)
    profile_image = models.TextField(default=None , null=True)
    user_type = models.CharField(choices=USER_CHOICES,max_length=10,default="INVESTOR")
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)