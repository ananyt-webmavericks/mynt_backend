from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InvestorKyc
from mynt_users.models import MyntUsers
from .serializers import InvestorKycSerializer
import random
import math
import datetime
import http.client
import json
import environ
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
env = environ.Env()
environ.Env.read_env()

class InvestorKycPanApiView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(id = request.data.get('user_id'))
            investor_kyc = InvestorKyc.objects.filter(user_id = request.data.get('user_id'))
            if investor_kyc:
                return Response({"status":"false","message":"investor kyc already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            data = {
                "pan_card":request.data.get('pan_card'),
                "birth_date":request.data.get('birth_date'),
                "birth_month":request.data.get('birth_month'),
                "birth_year":request.data.get('birth_year'),
                "user_id":user.id,
                "created_at":datetime.datetime.now(),
                "pan_card_verified":verify_pan_card(request.data.get('pan_card'))
            }
            serializer = InvestorKycSerializer(data=data)
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
            investor_kyc = InvestorKyc.objects.filter()
            serializer = InvestorKycSerializer(investor_kyc, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        try:
            investor_kyc = InvestorKyc.objects.get(user_id = request.data.get('user_id'))
            if request.data.get('pan_card'):
                investor_kyc.pan_card = request.data.get('pan_card')
            if request.data.get('birth_date'):
                investor_kyc.birth_date = request.data.get('birth_date')
            if request.data.get('birth_month'):
                investor_kyc.birth_month = request.data.get('birth_month')
            if request.data.get('birth_year'):
                investor_kyc.birth_year = request.data.get('birth_year')
            investor_kyc.pan_card_verified = verify_pan_card(request.data.get('pan_card'))
            investor_kyc.save()
            updated_kyc = InvestorKyc.objects.get(user_id = request.data.get('user_id'))
            serializer = InvestorKycSerializer(updated_kyc, many=False)
            return Response({"status":"true","message":"user kyc updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except investor_kyc.DoesNotExist:
            return Response({"status":"false","message":"User Kyc Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class GetInvestorKyc(APIView):
    def get(self, request, user_id ):
        try:
            investor_kyc = InvestorKyc.objects.get(user_id=user_id)
            serializer = InvestorKycSerializer(investor_kyc)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except InvestorKyc.DoesNotExist:
            return Response({"status":"false","message":"User Kyc Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

def verify_pan_card(pan_card):
    try:
        auth_token , user_id = authorize_signzy()

        conn = http.client.HTTPSConnection(env('SIGNZY_URL'))
        payload = json.dumps({
            "task": "fetch",
            "essentials": {
                "number": pan_card
            }
        })
        headers = {
            'Authorization': auth_token,
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/api/v2/patrons/"+user_id+"/panv2", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        if data['error']:
            return False
        

    except Exception as e:
        return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

def verify_bank_account(bank_account,ifsc_code):
    try:
        auth_token , user_id = authorize_signzy()
        return False
    except Exception as e:
        return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
def authorize_signzy():
    try:
        conn = http.client.HTTPSConnection(env('SIGNZY_URL'))
        payload = json.dumps({
            "username": env('SIGNZY_USERNAME'),
            "password": env('SIGNZY_PASSWORD')
        })
        headers = {
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/api/v2/patrons/login", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        return data['id'],data['userId']
    except Exception as e:
        return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class InvestorKycMobileApiView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(id = request.data.get('user_id'))
            investor_kyc = InvestorKyc.objects.filter(user_id = request.data.get('user_id'))
            if investor_kyc:
                return Response({"status":"false","message":"investor kyc already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            data = {
                "mobile_number":request.data.get('mobile_number'),
                "mobile_number_otp":generate_otp(),
                "user_id":user.id,
                "created_at":datetime.datetime.now(),
            }
            serializer = InvestorKycSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                ## ADD LOGIC TO SEND OTP
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        try :
            investor_kyc = InvestorKyc.objects.get(user_id = request.data.get('user_id'))
            investor_kyc.mobile_number  = request.data.get('mobile_number')
            investor_kyc.mobile_number_otp = generate_otp()
            investor_kyc.save()
            updated_kyc = InvestorKyc.objects.get(user_id = request.data.get('user_id'))
            ## ADD LOGIC TO SEND OTP
            serializer = InvestorKycSerializer(updated_kyc, many=False)
            return Response({"status":"true","message":"user kyc updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)
        except InvestorKyc.DoesNotExist:
            return Response({"status":"false","message":"User kyc Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


def generate_otp():
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    return random_str


class SendMobileOtp(APIView):
    def post(self, request, *args, **kwargs):
        try:
            investor_kyc = InvestorKyc.objects.get(user_id = request.data.get('user_id'))
            investor_kyc.mobile_number = request.data.get('mobile_number')
            investor_kyc.mobile_number_otp = generate_otp()
            investor_kyc.save()
            ## ADD LOGIC TO SEND OTP
            updated_kyc = InvestorKyc.objects.get(user_id = request.data.get('user_id'))
            serializer = InvestorKycSerializer(updated_kyc, many=False)
            return Response({"status":"true","message":"user kyc updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)
        except InvestorKyc.DoesNotExist:
            return Response({"status":"false","message":"User kyc Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyMobileOtp (APIView):
    def post(self, request, *args, **kwargs):
        try:
            investor_kyc = InvestorKyc.objects.get(user_id = request.data.get('user_id'))
            otp = request.data.get('otp')
            if otp == investor_kyc.mobile_number_otp:
                investor_kyc.mobile_number_verified = True
                investor_kyc.save()
                ## ADD LOGIC TO SEND OTP
                updated_kyc = InvestorKyc.objects.get(user_id = request.data.get('user_id'))
                serializer = InvestorKycSerializer(updated_kyc, many=False)
                return Response({"status":"true","message":"otp verified successfully!","data":serializer.data}, status=status.HTTP_200_OK)
            return Response({"status":"false","message":"Invalid OTP!"},status=status.HTTP_200_OK)
        except InvestorKyc.DoesNotExist:
            return Response({"status":"false","message":"User kyc Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class InvestorKycAddressApiView (APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(id = request.data.get('user_id'))
            investor_kyc = InvestorKyc.objects.filter(user_id = request.data.get('user_id'))
            if investor_kyc:
                return Response({"status":"false","message":"investor kyc already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            data = {
                "address_line_1":request.data.get('address_line_1'),
                "address_line_2":request.data.get('address_line_2'),
                "city":request.data.get('city'),
                "state":request.data.get('state'),
                "pincode":request.data.get('pincode'),
                "user_id":user.id,
                "created_at":datetime.datetime.now(),
            }
            serializer = InvestorKycSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        try:
            investor_kyc = InvestorKyc.objects.get(user_id = request.data.get('user_id'))
            if request.data.get('address_line_1'):
                investor_kyc.address_line_1 = request.data.get('address_line_1')
            if request.data.get('address_line_2'):
                investor_kyc.address_line_2 = request.data.get('address_line_2')
            if request.data.get('city'):
                investor_kyc.city = request.data.get('city')
            if request.data.get('state'):
                investor_kyc.state = request.data.get('state')
            if request.data.get('pincode'):
                investor_kyc.pincode = request.data.get('pincode')
            investor_kyc.save()
            updated_kyc = InvestorKyc.objects.get(user_id = request.data.get('user_id'))
            ## ADD LOGIC TO SEND OTP
            serializer = InvestorKycSerializer(updated_kyc, many=False)
            return Response({"status":"true","message":"user kyc updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)
        except InvestorKyc.DoesNotExist:
            return Response({"status":"false","message":"User kyc Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class InvestorKycBankVerificationApiView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(id = request.data.get('user_id'))
            investor_kyc = InvestorKyc.objects.filter(user_id = request.data.get('user_id'))
            if investor_kyc:
                return Response({"status":"false","message":"investor kyc already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            data = {
                "bank_name":request.data.get('bank_name'),
                "bank_account":request.data.get('bank_account'),
                "ifsc_code":request.data.get('ifsc_code'),
                "bank_account_verified":verify_bank_account(request.data.get('bank_account'),request.data.get('ifsc_code')),
                "user_id":user.id,
                "created_at":datetime.datetime.now(),
            }
            serializer = InvestorKycSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        try:
            investor_kyc = InvestorKyc.objects.get(user_id = request.data.get('user_id'))
            if request.data.get('bank_name'):
                investor_kyc.bank_name = request.data.get('bank_name')
            if request.data.get('bank_account'):
                investor_kyc.bank_account = request.data.get('bank_account')
            if request.data.get('ifsc_code'):
                investor_kyc.ifsc_code = request.data.get('ifsc_code')
            investor_kyc.bank_account_verified = verify_bank_account(request.data.get('bank_account'),request.data.get('ifsc_code'))
            investor_kyc.save()
            updated_kyc = InvestorKyc.objects.get(user_id = request.data.get('user_id'))
            serializer = InvestorKycSerializer(updated_kyc, many=False)
            return Response({"status":"true","message":"user kyc updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)
        except InvestorKyc.DoesNotExist:
            return Response({"status":"false","message":"User kyc Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)