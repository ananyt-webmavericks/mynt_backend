from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from company.models import Company
from .models import Payment
from campaign.models import Campaign
from .serializers import PaymentSerializer
from mynt_users.models import MyntUsers
from mynt_users.authentication import SafeJWTAuthentication
import datetime
import time
import http.client
import json
import environ

env = environ.Env()
environ.Env.read_env()

class CreateOrder(APIView):
    def post(self, request, args, *kwargs):
        try:
            user = MyntUsers.objects.get(id = request.data.get('user_id'))
            campaign = Campaign.objects.get(id = request.data.get('campaign_id'))
            ms = datetime.datetime.now()
            amount = request.data.get("amount")
            data = {
                "user_id":user.id,
                "campaign_id":campaign.id,
                "mynt_order_id":str(time.mktime(ms.timetuple()))+user.first_name,
                "amount":request.data.get("amount"),
                "created_at":datetime.datetime.now(),
                "updated_at":datetime.datetime.now(),
            }
            serializer = PaymentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                cashfree_order_id , payment_session_id = call_cashfree(user,amount,campaign.id)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetOrderDetails(APIView):
    def get(self, request, id):
        pass


class SuccessWebhook(APIView):
    def post(self, request, args, *kwargs):
        pass

def call_cashfree(user,amount,order_id):
    try:

        conn = http.client.HTTPSConnection(env('CASHFREE_ENDPOINT'))
        payload = json.dumps({
        "order_id": order_id,
        "order_amount": amount,
        "order_currency": "INR",
        "customer_details": {
            "customer_id": user.id,
            "customer_name": user.first_name,
            "customer_email": user.email,
            "customer_phone": "8696623400"
        },
        "order_meta": {
            "return_url": f"{env('CASHFREE_RETURN_URL')}?order_id={order_id}",
            "notify_url": env('CASHFREE_NOTIFY_URL')
        },
        "order_note": "enrollment"
        })
        headers = {
        'Content-Type': 'application/json',
        'x-api-version': '2022-09-01',
        'x-client-id': env('CASHFREE_CLIENT_ID'),
        'x-client-secret': env('CASHFREE_SECRET_ID')
        }
        conn.request("POST", "orders", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        print(user)
    except Exception as e:
        print(e)