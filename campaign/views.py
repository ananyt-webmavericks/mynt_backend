from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from company.models import Company
from .models import Campaign
from .serializers import CampaignSerializer
from mynt_users.models import MyntUsers
import datetime


class CampaignApiView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            company = Company.objects.filter(user_id = request.data.get('user_id')).get()
            
            campaign = Campaign.objects.filter(company_id = company.id)
            
            if campaign:
                return Response({"status":"false","message":"Campaign already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            data = {
                "company_id":company.id,
                "youtube_link":request.data.get('youtube_link'),
                "ama_date":request.data.get('ama_date'),
                "ama_meet_link":request.data.get('ama_meet_link'),
                "ama_youtube_video":request.data.get('ama_youtube_video'),
                "pitch":request.data.get('pitch'),
                "created_at":datetime.datetime.now()
                }
            serializer = CampaignSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        try:
            campaign = Campaign.objects.filter()
            serializer = CampaignSerializer(campaign, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        try:
            
            campaign = Campaign.objects.get(company_id__user_id__id = request.data.get('user_id'))

            if request.data.get('youtube_link'):
                campaign.youtube_link = request.data.get('youtube_link')

            if request.data.get('ama_date'):
                campaign.ama_date = request.data.get('ama_date')

            if request.data.get('ama_meet_link'):
                campaign.ama_meet_link = request.data.get('ama_meet_link')

            if request.data.get('ama_youtube_video'):
                campaign.ama_youtube_video = request.data.get('ama_youtube_video')

            if request.data.get('pitch'):
                campaign.pitch = request.data.get('pitch')
            
            campaign.save()
            updated_campaign = Campaign.objects.get(company_id__user_id__id = request.data.get('user_id'))
            serializer = CampaignSerializer(updated_campaign, many=False)
            return Response({"status":"true","message":"Campaign updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except Company.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    