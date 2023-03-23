from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Faqs
from company.models import Company
from campaign.models import Campaign
from mynt_users.models import MyntUsers
from .serializers import FaqsSerializers
import datetime

class FaqsApiView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(id = request.data.get('user_id'))
            company = Company.objects.filter(user_id = request.data.get('user_id')).first()
            if company is None:
                return Response({"status":"false","message":"Company not exists!"}, status=status.HTTP_400_BAD_REQUEST)

            campaign = Campaign.objects.filter(company_id = company).first()
            if campaign is None:
                return Response({"status":"false","message":"Campaign not exists!"}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                "campaign_id": campaign.id,
                "question":request.data.get('question'),
                "answer":request.data.get('answer'),
                "created_at":datetime.datetime.now()
            }
            serializer = FaqsSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        try:
            faqs = Faqs.objects.filter()
            serializer = FaqsSerializers(faqs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        try:
            faqs = Faqs.objects.get(id = request.data.get('faqs_id'))
            if request.data.get('question'):
                faqs.question = request.data.get('question')
            if request.data.get('answer'):
                faqs.answer = request.data.get('answer')
                 
            faqs.save()
            updated_faqs = Faqs.objects.get(id = request.data.get('faqs_id'))
            serializer = FaqsSerializers(updated_faqs, many=False)
            return Response({"status":"true","message":"Faq updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except Faqs.DoesNotExist:
            return Response({"status":"false","message":"Faq Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
