from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InvestorConsent
from mynt_users.models import MyntUsers
from .serializers import InvestorConsentSerializer
import datetime

class InvestorConsentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(id = request.data.get('user_id'))
            investor_consent = InvestorConsent.objects.filter(user_id = request.data.get('user_id'))
            if investor_consent:
                return Response({"status":"false","message":"consent already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            data = {
                "risk_consent":request.data.get('risk_consent'),
                "limited_transfer_consent":request.data.get('limited_transfer_consent'),
                "diversification_consent":request.data.get('diversification_consent'),
                "cancellation_consent":request.data.get('cancellation_consent'),
                "research_consent":request.data.get('research_consent'),
                "created_at":datetime.datetime.now(),
                "user_id":user.id
            }
            serializer = InvestorConsentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        try:
            consents = InvestorConsent.objects.filter()
            serializer = InvestorConsentSerializer(consents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        try:
            consent = InvestorConsent.objects.get(user_id = request.data.get('user_id'))
            consent.risk_consent = request.data.get('risk_consent')
            consent.limited_transfer_consent = request.data.get('limited_transfer_consent')
            consent.diversification_consent = request.data.get('diversification_consent')
            consent.cancellation_consent = request.data.get('cancellation_consent')
            consent.research_consent = request.data.get('research_consent')
            consent.save()
            consent = InvestorConsent.objects.get(user_id = request.data.get('user_id'))
            serializer = InvestorConsentSerializer(consent)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except InvestorConsent.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetConsentByUserId(APIView):
    def get(self, request, user_id):
        try:
            consent = InvestorConsent.objects.get(user_id = user_id)
            serializer = InvestorConsentSerializer(consent)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except InvestorConsent.DoesNotExist:
            return Response({"status":"false","message":"Consent Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)