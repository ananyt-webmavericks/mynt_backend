from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mynt_users.authentication import SafeJWTAuthentication
from company.models import Company
from .models import Campaign
from .serializers import CampaignSerializer, CampaignSerializerWithCompanySerializer
from deal_terms.models import DealTerms
from mynt_users.models import MyntUsers
import datetime
from documents.models import Documents
from company.models import Company
from company.serializers import CompanySerializers
from deal_terms.models import DealTerms
from deal_terms.serializers import DealTermsSerializer
from payment.models import Payment
from deal_type.serializers import DealTypeSerializer


class CampaignApiView(APIView):
    permission_classes = [SafeJWTAuthentication]
    
    def post(self, request, *args, **kwargs):
        try:
            company = Company.objects.get(id = request.data.get('company_id'))

            if company.status == "INACTIVE":
                return Response({"status":"false","message":"Company is Under Review yet!!"}, status=status.HTTP_400_BAD_REQUEST)
            
            document = Documents.objects.filter(company_id=request.data.get('company_id') ,agreement_status="SIGNED BY FOUNDER" )
            if document is None:
                return Response({"status":"false","message":"Please wait for Agreements to be Completed!!"}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                "company_id":company.id,
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
            campaigns = Campaign.objects.filter(status="LIVE")
            result = []
            for campaign in campaigns:
                campaign_serialiser = CampaignSerializer(campaign, many=False)
                company_details = Company.objects.get(id=campaign.company_id.id)
                company_serialiser = CompanySerializers(company_details,many=False)
                deal_terms = DealTerms.objects.filter(campaign_id=campaign.id).first()
                deal_terms_serialiser = DealTermsSerializer(deal_terms,many=False)
                deal_type = deal_terms.security_type
                deal_type_serialiser = DealTypeSerializer(deal_type,many=False)
                payments = Payment.objects.filter(campaign_id=campaign.id,status="COMPLETED")
                total_invested = 0
                total_investors = 0
                for payment in payments:
                    total_invested = payment.amount + total_invested
                    total_investors = total_investors + 1
                total_raised = (total_invested / int(deal_terms.target))/100
                data = {
                    "campaign":campaign_serialiser.data,
                    "company":company_serialiser.data,
                    "deal_terms":deal_terms_serialiser.data,
                    "deal_type":deal_type_serialiser.data,
                    "total_investors":total_investors,
                    "total_raised":total_raised
                }
                result.append(data)
            return Response({"status":"true","data":result}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
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


class GetAllCmapaignByStatus(APIView):
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


class GetCampaignWithAllDataByCampaignId(APIView):
    permission_classes = [SafeJWTAuthentication]

    def get(self, request, id):
        try:
            campaign = Campaign.objects.get(id = id)

            serializer = CampaignSerializerWithCompanySerializer(campaign)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Campaign.DoesNotExist:
            return Response({"status":"false","message":"Campaign Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetCampaignsCount(APIView):
    permission_classes = [SafeJWTAuthentication]
    def get(self, request, *args, **kwargs):
        try:
            campaignStatus=request.GET.get('status')
            count = Campaign.objects.filter(status=campaignStatus).count()
            data = {
                "count":count
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)