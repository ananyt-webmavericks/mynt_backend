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
from mynt_users.authentication import SafeJWTAuthentication
import datetime

class FaqsApiView(APIView):
    permission_classes = [SafeJWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            campaign = Campaign.objects.get(id = request.data.get('campaign_id'))
            
            faqs = request.data.get('faqs')
            errors = []
            res_data = []
            if isinstance(faqs, list):
                for i in faqs:
                    try:
                        data = {
                            "campaign_id": campaign.id,
                            "question": i['question'],
                            "answer": i['answer'],
                            "created_at":datetime.datetime.now()
                        }
                        serializer = FaqsSerializers(data=data)
                        if serializer.is_valid():
                            serializer.save()
                            res_data.append(serializer.data)
                        else:
                            errors.append(serializer.errors)

                    except Exception as e:
                        continue
            else:
                return Response({"status":"false","message":"Invalid format of property faqs!"}, status=status.HTTP_400_BAD_REQUEST)
                
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(res_data, status=status.HTTP_201_CREATED)
        except Campaign.DoesNotExist:
            return Response({"status":"false","message":"Campaign Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
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
            if request.data.get('campaign_id'):
                campaign = Campaign.objects.filter(id = request.data.get('campaign_id')).first()
                if campaign:
                    faqs.campaign_id = campaign
                else:
                    return Response({"status":"false","message":"Campaign Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
                 
            faqs.save()
            updated_faqs = Faqs.objects.get(id = request.data.get('faqs_id'))
            serializer = FaqsSerializers(updated_faqs, many=False)
            return Response({"status":"true","message":"Faq updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except Faqs.DoesNotExist:
            return Response({"status":"false","message":"Faq Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
