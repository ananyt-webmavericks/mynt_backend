from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from company.models import Company
from .models import Press
from .serializers import Pressserializer
from mynt_users.models import MyntUsers
from mynt_users.authentication import SafeJWTAuthentication
import datetime


class PressApiView(APIView):
    permission_classes = [SafeJWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            company = Company.objects.get(id = request.data.get('company_id'))

            banners = request.data.get('banners')
            errors = []
            res_data = []
            if isinstance(banners, list):
                for i in banners:
                    try:
                        data = {
                                "company_id": company.id,
                                "title":request.data.get('title'),
                                "link":request.data.get('link'),
                                "description":request.data.get('description'),
                                "banner":request.data.get('banner'),
                                "created_at":datetime.datetime.now()
                            }
                        serializer = Pressserializer(data=data)
                        if serializer.is_valid():
                            serializer.save()
                            res_data.append(serializer.data)
                        else:
                            errors.append(serializer.errors)

                    except Exception as e:
                        continue
            else:
                return Response({"status":"false","message":"Invalid format of property documents!"}, status=status.HTTP_400_BAD_REQUEST)
                
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(res_data, status=status.HTTP_201_CREATED)
            
        except Company.DoesNotExist:
            return Response({"status":"false","message":"Company Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        try:
            press = Press.objects.filter()
            serializer = Pressserializer(press, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        try:
            press = Press.objects.get(id = request.data.get('press_id'))
            if request.data.get('title'):
                press.title = request.data.get('title')
            if request.data.get('link'):
                press.link = request.data.get('link')
            if request.data.get('description'):
                press.description = request.data.get('description')
            if request.data.get('banner'):
                press.banner = request.data.get('banner')
            if request.data.get('company_id'):
                company = Company.objects.filter(id = request.data.get('company_id')).first()
                if company:
                    press.company_id = company
                else:
                    return Response({"status":"false","message":"Company Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
                         
            press.save()
            updated_press = Press.objects.get(id = request.data.get('press_id'))
            serializer = Pressserializer(updated_press, many=False)
            return Response({"status":"true","message":"Press updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except Press.DoesNotExist:
            return Response({"status":"false","message":"Press Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetPressbyCompanyId(APIView):
    permission_classes = [SafeJWTAuthentication]

    def get(self, request, id):
        try:
            press = Press.objects.filter(company_id = id).all()
            if press:
                serializer = Pressserializer(press, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"status":"false","message":"Press Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)