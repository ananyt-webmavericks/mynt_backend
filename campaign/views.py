from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mynt_users.authentication import SafeJWTAuthentication
from company.models import Company
from .models import Campaign
from .serializers import CampaignSerializer
from deal_terms.models import DealTerms
from mynt_users.models import MyntUsers
import datetime


class CampaignApiView(APIView):
    permission_classes = [SafeJWTAuthentication]
    
    def post(self, request, *args, **kwargs):
        try:
            company = Company.objects.get(id = request.data.get('company_id'))
            
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
            return Response({"status":"false","message":"Company Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
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
            
            campaign = Campaign.objects.get(id = request.data.get('campaign_id'))

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
            
            if request.data.get('status'):
                if request.data.get('status') == "LIVE":
                    deal = DealTerms.objects.filter(campaign_id=campaign.id).exists()
                    if deal:
                        campaign.status = request.data.get('status')
                    else:
                        return Response({"status":"false","message":"Campaign Deal Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
                else:
                    campaign.status = request.data.get('status')
            
            if request.data.get('company_id'):
                company = Company.objects.filter(id = request.data.get('company_id')).first()
                if company:
                    campaign.company_id = company
                else:
                    return Response({"status":"false","message":"Company Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
            
            campaign.save()
            updated_campaign = Campaign.objects.get(id = request.data.get('campaign_id'))
            serializer = CampaignSerializer(updated_campaign, many=False)
            return Response({"status":"true","message":"Campaign updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except Campaign.DoesNotExist:
            return Response({"status":"false","message":"Campaign Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class CampaignByCompanyId(APIView):
    permission_classes = [SafeJWTAuthentication]

    def get(self, request, id):
        try:
            campaign = Campaign.objects.filter(company_id = id).all()

            if campaign:
                serializer = CampaignSerializer(campaign, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"status":"false","message":"Campaign Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class GetCmapaignById(APIView):
    permission_classes = [SafeJWTAuthentication]

    def get(self, request, id):
        try:
            campaign = Campaign.objects.get(id = id)

            serializer = CampaignSerializer(campaign)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Campaign.DoesNotExist:
            return Response({"status":"false","message":"Campaign Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetAllCmapaignbyStatus(APIView):
    permission_classes = [SafeJWTAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            campaign = Campaign.objects.filter(status=request.data.get('status'))
            if campaign:
                serializer = CampaignSerializer(campaign, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"status":"false","message":"Campaign Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
