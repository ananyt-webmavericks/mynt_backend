from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from company.models import Company
from campaign.models import Campaign
from .models import Rewards
from .serializers import Rewardsserializer
from mynt_users.models import MyntUsers
from mynt_users.authentication import SafeJWTAuthentication
import datetime


class RewardsApiView(APIView):
    permission_classes = [SafeJWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:

            campaign = Campaign.objects.get(id = request.data.get('campaign_id'))
            
            data = {
                "campaign_id": campaign.id,
                "amount":request.data.get('amount'),
                "product_name":request.data.get('product_name'),
                "discounted_price":request.data.get('discounted_price'),
                "created_at":datetime.datetime.now()
            }
            serializer = Rewardsserializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Campaign.DoesNotExist:
            return Response({"status":"false","message":"Campaign Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        try:
            rewards = Rewards.objects.filter()
            serializer = Rewardsserializer(rewards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        try:
            reward = Rewards.objects.get(id = request.data.get('reward_id'))
            if request.data.get('amount'):
                reward.amount = request.data.get('amount')
            if request.data.get('product_name'):
                reward.product_name = request.data.get('product_name')
            if request.data.get('discounted_price'):
                reward.discounted_price = request.data.get('discounted_price')
            if request.data.get('campaign_id'):
                campaign = Campaign.objects.filter(id = request.data.get('campaign_id')).first()
                if campaign:
                    reward.campaign_id = campaign
                else:
                    return Response({"status":"false","message":"Campaign Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)

            reward.save()
            updated_reward = Rewards.objects.get(id = request.data.get('reward_id'))
            serializer = Rewardsserializer(updated_reward, many=False)
            return Response({"status":"true","message":"Reward updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except Rewards.DoesNotExist:
            return Response({"status":"false","message":"Reward Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetRewardsbyCampaignId(APIView):
    permission_classes = [SafeJWTAuthentication]

    def get(self, request, id):
        try:
            rewards = Rewards.objects.filter(campaign_id = id).all()
            if rewards:
                serializer = Rewardsserializer(rewards, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"status":"false","message":"Rewards Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)