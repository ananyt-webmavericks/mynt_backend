from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from company.models import Company
from campaign.models import Campaign
from .models import DealTerms
from deal_type.models import DealType
from .serializers import DealTermsSerializer, DealTermsRefrenceSerializer
from mynt_users.models import MyntUsers
from mynt_users.authentication import SafeJWTAuthentication
import datetime


class DealTermsApiView(APIView):
    permission_classes = [SafeJWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:            
            campaign = Campaign.objects.get(id = request.data.get('campaign_id'))
            
            deal_type = DealType.objects.filter(id = request.data.get('security_type_id')).first()
            if deal_type is None:
                return Response({"status":"false","message":"Security Type is not exists!"}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                "campaign_id":campaign.id,
                "security_type": deal_type.id,
                "discount":request.data.get('discount'),
                "valuation_cap":request.data.get('valuation_cap'),
                "min_subscription":request.data.get('min_subscription'),
                "target":request.data.get('target'),
                "end_date":request.data.get('end_date'),
                "created_at":datetime.datetime.now()
                }
            serializer = DealTermsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Campaign.DoesNotExist:
            return Response({"status":"false","message":"Campaign is not exists!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        try:
            dealterms = DealTerms.objects.filter()
            serializer = DealTermsRefrenceSerializer(dealterms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        try:
            
            dealterm = DealTerms.objects.get(id = request.data.get('deal_term_id'))

            if request.data.get('security_type'):
                deal_type = DealType.objects.filter(id=request.data.get('security_type_id')).first()
                
                if deal_type:
                    dealterm.security_type = deal_type.id
                else:
                    return Response({"status":"false","message":"Security Type is not exists!"}, status=status.HTTP_400_BAD_REQUEST)

            if request.data.get('campaign_id'):
                campaign = Campaign.objects.filter(id=request.data.get('campaign_id')).first()
                
                if campaign:
                    dealterm.campaign_id = campaign
                else:
                    return Response({"status":"false","message":"Campaign Doesn't Exist!"}, status=status.HTTP_400_BAD_REQUEST)


            if request.data.get('discount'):
                dealterm.discount = request.data.get('discount')

            if request.data.get('valuation_cap'):
                dealterm.valuation_cap = request.data.get('valuation_cap')

            if request.data.get('min_subscription'):
                dealterm.min_subscription = request.data.get('min_subscription')

            if request.data.get('target'):
                dealterm.target = request.data.get('target')
                
            if request.data.get('end_date'):
                dealterm.end_date = request.data.get('end_date')
            
            dealterm.save()
            updated_deal_term = DealTerms.objects.get(id = request.data.get('deal_term_id'))
            serializer = DealTermsSerializer(updated_deal_term, many=False)
            return Response({"status":"true","message":"Deal Terms updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except DealTerms.DoesNotExist:
            return Response({"status":"false","message":"Deal Terms Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    