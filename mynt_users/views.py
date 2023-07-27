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
from django.contrib.auth.hashers import check_password, make_password
from .mail import send_mail
from payment.models import Payment
from documents.models import Documents

class MyntUsersApiView(APIView):
    permission_classes = [SafeJWTAuthentication]

    def get (self, request, *args, **kwargs):
        filter = request.GET.get('user_type')
        users = MyntUsers.objects.filter()
        if(filter):
            users = MyntUsers.objects.filter(user_type=filter)
        serializer = MyntUsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def patch(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(id=request.data.get('user_id'))
            if request.data.get('profile_image'):
                user.profile_image = request.data.get('profile_image')
            if request.data.get('secondary_email'):
                secondary_email = request.data.get('secondary_email')
                all_users = MyntUsers.objects
                email_check = all_users.filter(email=secondary_email).exists()

                if user.email == request.data.get('secondary_email') or email_check:
                    return Response({"status":"false","message":"User Email already Exist!"},status=status.HTTP_404_NOT_FOUND)
                
                user.secondary_email = request.data.get('secondary_email')
                user.secondary_email_verified = False
            if request.data.get('country'):
                user.country = request.data.get('country')
            if request.data.get('nationality'):
                user.nationality = request.data.get('nationality')
            user.save()
            updated_user = MyntUsers.objects.get(id=request.data.get('user_id'))
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
                    data = serializer.data
                    if updated_user.user_type == 'FOUNDER':
                        company = Company.objects.filter(user_id=updated_user.id).first()
                        if company is None:
                            data['company_id'] = "User has Doesn't Exist Company!"
                        else:
                            data['company_id'] = company.id
                    return Response({"status":"true","message":"OTP verified!","data":data,
                                     "access_token": str(refresh.access_token),
                                     "refresh_token": str(refresh)},status=status.HTTP_200_OK)
                return Response({"status":"false","message":"Invalid OTP!"},status=status.HTTP_200_OK)
            return Response({"status":"false","message":"otp can not be empty!"},status=status.HTTP_400_BAD_REQUEST)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SecondaryEmailVerifyView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(secondary_email=request.data.get('email'))
            if request.data.get('otp'):
                otp = request.data.get('otp')
                if(otp == user.secondary_email_otp):
                    user.secondary_email_verified = True
                    user.email = request.data.get('email')
                    user.save()
                    updated_user = MyntUsers.objects.get(email=request.data.get('email'))
                    serializer = MyntUsersSerializer(updated_user, many=False)
                    data = serializer.data
                    
                    return Response({"status":"true","message":"Email Updated successfully!","data":data,},status=status.HTTP_200_OK)
                return Response({"status":"false","message":"Invalid OTP!"},status=status.HTTP_200_OK)
            return Response({"status":"false","message":"otp can not be empty!"},status=status.HTTP_400_BAD_REQUEST)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SendOTPOnMail(APIView):
    def post(self, request, *args, **kwargs):
        try:
            if request.data.get('email'):
                user = MyntUsers.objects.get(email=request.data.get('email'))
                #add logic to send email templates
                user.email_otp = generate_otp()
                user.email_verified = False
                user.save() 
                otp = user.email_otp
                email = user.email
            elif(request.data.get('secondary_email')):
                user = MyntUsers.objects.get(secondary_email=request.data.get('secondary_email'))
                #add logic to send email templates
                user.secondary_email_otp = generate_otp()
                user.secondary_email_verified = False
                user.save()
                otp = user.secondary_email_otp
                email = user.secondary_email


            #send email to User for OTP
            context = {
                    'name' : user.first_name,
                    'otp':otp}
            send_mail(template_name='verification.html',context=context,email=email,name=f"{user.first_name} {user.last_name}",subject="Verification Code",text_part=f"Verification Code {email}")
            
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
            login_type = request.data.get('login_type')
            if user.user_type != login_type:
                return Response({"status":"false","message":f"This User is not Valid {login_type}!"},status=status.HTTP_404_NOT_FOUND)

            # Check Founder Company is Active
            if user.user_type == 'FOUNDER':
                company = Company.objects.filter(user_id=user.id).first()
                if company:
                    if company.status == 'INACTIVE':
                        return Response({"status":"false","message":"Your Company is Under Review"},status=status.HTTP_200_OK)
                else:
                    return Response({"status":"false","message":"User Doesn't Exist any Company!"},status=status.HTTP_404_NOT_FOUND)
           
            # Login Code for ADMIN User
            if user.user_type == 'ADMIN':
                is_password= check_password(request.data.get('password'),user.password)
                if is_password:
                    refresh = RefreshToken.for_user(user=user)
                    serializer = MyntUsersSerializer(user)
                    return Response({"status":"true","message":"Password verified!","data":serializer.data,
                                     "access_token": str(refresh.access_token),
                                     "refresh_token": str(refresh)},status=status.HTTP_200_OK)
                else:
                    return Response({"status":"false","message":"Incorrect Password!"},status=status.HTTP_404_NOT_FOUND)

                
            if user.social_login is False:
                user.email_otp = generate_otp()
                user.save()
                #send email to User for OTP
                context = {
                        'name' : user.first_name,
                        'otp':user.email_otp}
                send_mail(template_name='verification.html',context=context,email=user.email,name=f"{user.first_name} {user.last_name}",subject="Verification Code",text_part=f"Verification Code {user.email}")
                
                return Response({"status":"true","message":"Please veirfy OTP on mail!"},status=status.HTTP_200_OK)
            
            serializer = MyntUsersSerializer(user)

            if user.social_login is True:
                refresh = RefreshToken.for_user(user=user)

                return Response({"status":"true","message":"Successfully logged In","data":serializer.data,
                                    "access_token": str(refresh.access_token),
                                    "refresh_token": str(refresh)},status=status.HTTP_200_OK)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class MyntUserCreateApiview(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = {
                'first_name': request.data.get('first_name'), 
                'last_name': request.data.get('last_name'), 
                'email':request.data.get('email'),
                "social_login":request.data.get('social_login'),
                "user_type":request.data.get('user_type')
            }

            if(request.data.get('social_login') is False):
                
                # Admin User Create
                if request.data.get('user_type') == 'ADMIN':
                    if request.data.get('password'):
                        hash_password = make_password(password=request.data.get('password'))
                        data['password'] = hash_password
                    else:
                        return Response({"status":"false","message":"Password field is required."},status=status.HTTP_400_BAD_REQUEST)
                else:
                    data['email_otp'] = generate_otp()

            if(request.data.get('profile_image')):
                data['profile_image'] = request.data.get('profile_image')
            if(request.data.get('social_login') is True):
                data['email_verified'] = True
            data["created_at"] = datetime.datetime.now()

            serializer = MyntUsersSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

                #Send the Welcome Email
                context = {
                        'name' : request.data.get('first_name') }
                send_mail(template_name='welcome_mail.html',context=context,email=request.data.get('email'),name=f"{request.data.get('first_name')} {request.data.get('last_name')}",subject="Welcome to Mynt Invest",text_part=f"Welcome to Mynt Invest {request.data.get('email')}")
                
                # If social login is True raise the token
                if(request.data.get('social_login') is True):
                    user = MyntUsers.objects.filter(email = request.data.get('email')).first()
                    refresh = RefreshToken.for_user(user=user)
                    return Response({"status":"true","message":"Successfully logged In","data":serializer.data,
                                        "access_token": str(refresh.access_token),
                                        "refresh_token": str(refresh)},status=status.HTTP_200_OK)
                
                # Send the OTP mail if social login is False
                if(request.data.get('social_login') is False) and request.data.get('user_type') != 'ADMIN':
                    context = {
                            'name' : data['first_name'],
                            'otp': data['email_otp']}
                    send_mail(template_name='verification.html',context=context,email=data['email'],name=f"{data['first_name']} {data['last_name']}",subject="Verification Code",text_part=f"Verification Code {data['email']}")
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetUsersCount(APIView):
    def get(self, request, *args, **kwargs):
        try :
            user_type=request.GET.get('user_type')
            count = MyntUsers.objects.filter(user_type=user_type).count()
            data = {
                "count":count
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetUserPortfolio(APIView):
    def get(self, request, id):
        try:
            user = MyntUsers.objects.get(id=id)
            payments = Payment.objects.filter(user_id=user.id , status = "COMPLETED")
            data = []
            for payment in payments:
                result = {
                    "company_logo":payment.campaign_id.company_id.company_logo,
                    "company_name":payment.campaign_id.company_id.company_name,
                    "amount":payment.amount,
                    "enrollment_date":payment.updated_at,
                    "documents":[]
                }
                data.append(result)
            result = {
                "data":data
            }
            return Response(result, status=status.HTTP_200_OK)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class GetAgreementStatus(APIView):
    def get(self,request,id):
        try:
            user = MyntUsers.objects.get(id=id)
            if user.user_type != "FOUNDER":
                return Response({"status":"false","message":"User type is not Founder!"},status=status.HTTP_400_BAD_REQUEST)
            company = Company.objects.filter(user_id=user.id).first()
            if company.status != "ACTIVE":
                return Response({"status":"false","message":"Your Company is Under Review!"},status=status.HTTP_400_BAD_REQUEST)
            document = Documents.objects.filter(company_id=company.id,document_type="AGREEMENTS").first()
            result = {
                "document":document
            }
            return Response(result, status=status.HTTP_200_OK)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)