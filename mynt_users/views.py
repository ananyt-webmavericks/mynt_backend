from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MyntUsers
from .serializers import MyntUsersSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from company.models import Company
import random
import math
import datetime
from mynt_users.authentication import SafeJWTAuthentication

class MyntUsersApiView(APIView):

    def get (self, request, *args, **kwargs):
        users = MyntUsers.objects.filter()
        serializer = MyntUsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'first_name': request.data.get('first_name'), 
            'last_name': request.data.get('last_name'), 
            'email':request.data.get('email'),
            "social_login":request.data.get('social_login'),
            "user_type":request.data.get('user_type')
        }

        if(request.data.get('social_login') is False):
            data['email_otp'] = generate_otp()
        if(request.data.get('profile_image')):
             data['profile_image'] = request.data.get('profile_image')
        if(request.data.get('social_login') is True):
            data['email_verified'] = True
        data["created_at"] = datetime.datetime.now()
        serializer = MyntUsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(id=request.data.get('user_id'))
            if request.data.get('profile_image'):
                user.profile_image = request.data.get('profile_image')
            if request.data.get('email'):
                user.email = request.data.get('email')
                user.email_verified = False
            if request.data.get('country'):
                user.country = request.data.get('country')
            if request.data.get('nationality'):
                user.nationality = request.data.get('nationality')
            user.save()
            updated_user = MyntUsers.objects.get(email=request.data.get('email'))
            serializer = MyntUsersSerializer(updated_user, many=False)
            return Response({"status":"true","message":"user updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)



def generate_otp():
        digits = [i for i in range(0, 10)]
        random_str = ""
        for i in range(6):
            index = math.floor(random.random() * 10)
            random_str += str(digits[index])
        return random_str

class EmailVerifyView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(email=request.data.get('email'))
            if request.data.get('otp'):
                otp = request.data.get('otp')
                if(otp == user.email_otp):
                    user.email_verified = True
                    user.save()

                    updated_user = MyntUsers.objects.get(email=request.data.get('email'))
                    serializer = MyntUsersSerializer(updated_user, many=False)
                    refresh = RefreshToken.for_user(user=user)

                    return Response({"status":"true","message":"OTP verified!","data":serializer.data,
                                     "access_token": str(refresh.access_token),
                                     "refresh_token": str(refresh)},status=status.HTTP_200_OK)
                return Response({"status":"false","message":"Invalid OTP!"},status=status.HTTP_200_OK)
            return Response({"status":"false","message":"otp can not be empty!"},status=status.HTTP_400_BAD_REQUEST)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SendOTPOnMail(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(email=request.data.get('email'))
            #add logic to send email templates
            user.email_otp = generate_otp()
            user.email_verified = False
            user.save()
            return Response({"status":"true","message":"OTP sent successfully!!"},status=status.HTTP_200_OK)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetUserById(APIView):
    permission_classes = [SafeJWTAuthentication]

    def get(self, request, id):
        try:
            user = MyntUsers.objects.get(id=id)
            serializer = MyntUsersSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserByEmail(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(email=request.data.get('email'))
            if user.user_type == 'FOUNDER':
                company = Company.objects.filter(user_id=user.id).first()
                if company:
                    if company.status == 'INACTIVE':
                        return Response({"status":"false","message":"Your Company is Under Review"},status=status.HTTP_200_OK)
                else:
                    return Response({"status":"false","message":"User Doesn't Exist any Company!"},status=status.HTTP_404_NOT_FOUND)
                    
            if user.social_login is False:
                # user.email_otp = generate_otp()
                user.email_otp = 1234
                user.save()
                return Response({"status":"true","message":"Please veirfy OTP on mail!"},status=status.HTTP_200_OK)
            serializer = MyntUsersSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)