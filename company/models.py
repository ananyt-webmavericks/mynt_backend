from django.db import models

from mynt_users.models import MyntUsers


STATUS = (
    ("ACTIVE","ACTIVE"),
    ("INACTIVE","INACTIVE")
)

# Create your models here.

class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(MyntUsers , on_delete=models.CASCADE)
    company_logo = models.TextField(default=None)
    founder_linked_in_profile = models.TextField(default=None)
    company_name = models.CharField(max_length=100 , default=None)
    company_linked_in_profile = models.TextField(default=None)
    website_url = models.TextField(default=None)
    previous_funding = models.TextField(default=None,)
    product_description = models.TextField(default=None)
    traction_description = models.TextField(default=None)
    revenue = models.CharField(max_length=12 , default='0')
    reason_for_community_round = models.TextField(default=None)
    reason_for_mynt = models.TextField(default=None)
    existing_commitments = models.TextField(default=None)
    company_pitch = models.TextField(default=None)
    country = models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    pincode = models.CharField(max_length=6,null=True)
    company_address = models.TextField(null=True)
    facebook_link = models.TextField(null=True)
    instagram_link = models.TextField(null=True)
    legal_name = models.CharField(max_length=100,null=True)
    cin = models.CharField(max_length=22,null=True)
    date_of_incorporation = models.DateField(null=True)
    incorporation_type = models.CharField(max_length=50,null=True)
    sector = models.CharField(max_length=50,null=True)
    invested_so_far = models.CharField(max_length=12,null=True)
    number_of_employees = models.CharField(max_length = 5, null=True)
    status = models.CharField(choices=STATUS, max_length=20, default="INACTIVE")
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)