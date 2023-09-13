from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Interest
from mynt_users.models import MyntUsers
from .serializers import InterestSerializer
import datetime
from campaign.models import Campaign

class CreateInterest(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(id = request.data.get('user_id'))
            interest = Interest.objects.filter(investor_id = request.data.get('user_id'))
            campaign = Campaign.objects.get(id = request.data.get('campaign_id'))
            if interest:
                return Response({"status":"false","message":"Interest already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            data = {
                "campaign_id":campaign.id,
                "company_name":request.data.get("company_name"),
                "applied_date":datetime.datetime.now(),
                "investor_first_name":request.data.get("investor_first_name"),
                "investor_last_name":request.data.get("investor_last_name"),
                "investor_email":request.data.get("investor_email"),
                "investor_mobile_number":request.data.get("investor_mobile_number"),
                "created_at":datetime.datetime.now(),
                "investor_id":user.id
            }
            serializer = InterestSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Campaign.DoesNotExist:
            return Response({"status":"false","message":"Campaign Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CheckInterest(APIView):
    def get(self, request, user_id,campaign_id):
        try:
            user = MyntUsers.objects.get(id = user_id)
            campaign = Campaign.objects.get(id=campaign_id)
            check_interest = Interest.objects.get(campaign_id=campaign.id,investor_id=user.id)
            serializer = InterestSerializer(check_interest)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Interest.DoesNotExist:
            return Response({"status":"false","message":"Interest Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Campaign.DoesNotExist:
            return Response({"status":"false","message":"Campaign Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetAllInterest(APIView):
    def get(self, request, *args, **kwargs):
        try:
            interest = Interest.objects.filter()
            serializer = InterestSerializer(interest, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)