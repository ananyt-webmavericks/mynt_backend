from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Campaign
from payment.models import Payment
from mynt_users.models import MyntUsers
from .serializers import CampaignDocumentSerializers
from mynt_users.authentication import SafeJWTAuthentication
import datetime

class CampaignDocument(APIView):
    permission_classes = [SafeJWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            campaign = Campaign.objects.get(id = request.data.get('campaign_id'))
            payment = Payment.objects.filter(campaign_id = campaign.id , status="COMPLETED")
            for item in payment:
               data = {
                   "user_id" : item.user_id.id,
                   "agreement_status" : "UPLOADED BY FOUNDER",
                   "agreement_url":request.data.get('document_url'),
                   "agreement_name":request.data.get('document_name'),
                   "campaign_id":request.data.get('campaign_id'),
                   "created_at":datetime.datetime.now()
               }
               serializer = CampaignDocumentSerializers(data=data)
               if serializer.is_valid():
                  serializer.save()
               else:
                  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status":"true","message":"Agreements Sent Across"},status=status.HTTP_200_OK)
               
        except Campaign.DoesNotExist:
            return Response({"status":"false","message":"Campaign Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)