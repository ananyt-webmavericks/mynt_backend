from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from company.models import Company
from .models import Payment
from campaign.models import Campaign
from .serializers import PaymentSerializer, InvestorPaymentSerializer
from mynt_users.models import MyntUsers
from investor_kyc.models import InvestorKyc
from mynt_users.authentication import SafeJWTAuthentication
import datetime
import time
import http.client
import json
import environ
import requests
from .mail import send_mail

env = environ.Env()
environ.Env.read_env()

class CreateOrder(APIView):
    permission_classes = [SafeJWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(id = request.data.get('user_id'))
            campaign = Campaign.objects.get(id = request.data.get('campaign_id'))

            if campaign.status != "LIVE":
                return Response({"status":"false","message":"Campaign is not Live anymore!"},status=status.HTTP_404_NOT_FOUND)

            #Check User KYC is completed or not
            investor_kyc = InvestorKyc.objects.filter(user_id = user.id).first()
            if investor_kyc:
                if investor_kyc.mobile_number_verified is not True and investor_kyc.bank_account_verified is not True and investor_kyc.pan_card_verified is not True and  investor_kyc.aadhaar_card_verified is not True:
                    return Response({"status":"false","message":"Complete your KYC first."},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"status":"false","message":"KYC is pending."},status=status.HTTP_404_NOT_FOUND)
            
            payment = Payment.objects.filter(user_id=request.data.get('user_id'),campaign_id=request.data.get('campaign_id') , status="COMPLETED" ).first()

            if payment:
                return Response({"status":"false","message":"Already Invested in this Campaign!"},status=status.HTTP_400_BAD_REQUEST)
            
            payment = Payment.objects.filter(user_id=request.data.get('user_id'),campaign_id=request.data.get('campaign_id') , status="PENDING" ).first()
            if payment:
                return Response({"status":"false","message":"Please wait while we confirm the payment status!!"},status=status.HTTP_400_BAD_REQUEST)
           
            ms = datetime.datetime.now()
            total_amount = request.data.get("total_amount")
            mobile_number = investor_kyc.mobile_number
            order_id = str(int(time.mktime(ms.timetuple())))+'_'+user.first_name
            data = {
                "user_id":user.id,
                "campaign_id":campaign.id,
                "mynt_order_id":order_id,
                "amount":request.data.get("amount"),
                "total_amount":total_amount,
                "created_at":datetime.datetime.now(),
                "updated_at":datetime.datetime.now(),
            }
            serializer = PaymentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                cashfree_order_id , payment_session_id = call_cashfree(user,total_amount,order_id,mobile_number)
                payment = Payment.objects.filter(mynt_order_id=order_id).first()
                if payment:
                    payment.cashfree_order_id = cashfree_order_id
                    payment.payment_session_id = payment_session_id
                    payment.save()
                    serializer = PaymentSerializer(payment)
                    return Response({"status":"true","message":"Payment Created Succesfully","data":serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status":"false","message":f"Payment Doesn't Exist for this mynt_order_id {order_id}"},status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetOrderDetails(APIView):
    def get(self, request, order_id):
        try:
            payment = Payment.objects.get(mynt_order_id = order_id)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response({"status":"false","message":"Payment Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SuccessWebhook(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data.get('data')
            order_data = data['order']
            payment_data = data['payment']
            payment = Payment.objects.filter(mynt_order_id = order_data['order_id']).first()
            if payment:
                payment_status = payment_data['payment_status']

                if payment_status == "SUCCESS":
                    payment.status = "COMPLETED"

                elif payment_status == "FAILED":
                    payment.status = "FAILED"

                else :
                    payment.status = "PENDING"

                payment.save()
                updated_payment = Payment.objects.filter(mynt_order_id = order_data['order_id']).first()
                serializer = PaymentSerializer(updated_payment, many=False)
                user = MyntUsers.objects.filter(id=payment.user_id).first()
                campaign = Campaign.objects.filter(id=payment.campaign_id).first()
                company = Company.objects.filter(id=campaign.company_id).first()
                context = {
                    "investor_name":f"{user.first_name} {user.last_name}",
                    "company_name":company.company_name
                }

                failed_context = {
                    "investor_name":f"{user.first_name} {user.last_name}",
                    "company_name":company.company_name,
                    "investment_amount":payment.amount
                }

                if payment_data['payment_status'] == "SUCCESS":
                    send_mail(template_name='contract.html',context=context,email=user.email,name=f"{user.first_name} {user.last_name}",subject="Payment Confirmation For Investment on Mynt",text_part=f"Payment Confirmation For Investment on Mynt {user.email}")
                else:
                    send_mail(template_name='payment_failed.html',context=failed_context,email=user.email,name=f"{user.first_name} {user.last_name}",subject="Payment Failed For Investment on Mynt",text_part=f"Payment Failed For Investment on Mynt {user.email}")
                return Response({"status":"true","message":"Payment updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

            else:
                return Response({"status":"false","message":"Payment Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)



def call_cashfree(user,total_amount,order_id,mobile_number):
    try:

        url = f"{env('CASHFREE_ENDPOINT')}orders"

        print(url)

        payload = json.dumps({
        "order_id": order_id,
        "order_amount": total_amount,
        "order_currency": "INR",
        "customer_details": {
            "customer_id": str(user.id),
            "customer_name": str(user.first_name),
            "customer_email": str(user.email),
            "customer_phone": f"+{mobile_number}"
        },
        "order_meta": {
            "return_url": env('CASHFREE_RETURN_URL'),
            "notify_url": env('CASHFREE_NOTIFY_URL')
        },
        "order_note": "enrollment"
        })

        headers = {
        'x-api-version': env('CASHFREE_APP_VERSION'),
        'x-client-id': env('CASHFREE_CLIENT_ID'),
        'x-client-secret': env('CASHFREE_SECRET_ID'),
        'Content-Type': 'application/json'
        }

        print(payload)
        print(headers)

        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()
        print(data)
        
        return data['cf_order_id'], data['payment_session_id']
    except Exception as e:
        return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetAllPaymentDetails(APIView):
    permission_classes = [SafeJWTAuthentication]
    
    def get(self, request, *args, **kwargs):
        try:
            payment = Payment.objects.filter()
            serializer = PaymentSerializer(payment, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class InvestorPaymentDetailApiView(APIView):
    permission_classes = [SafeJWTAuthentication]

    def get(self, request, user_id):
        try:
            payment = Payment.objects.filter(user_id = user_id).all()

            if payment.exists() == False:
                return Response({"status":"false","message":"User's Payment Detail Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
            
            serializer = InvestorPaymentSerializer(payment, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
