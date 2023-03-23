from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from company.models import Company
from .models import People
from .serializers import Peopleserializer
from mynt_users.models import MyntUsers
import datetime


class PeopleApiView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(id = request.data.get('user_id'))
            company = Company.objects.filter(user_id = request.data.get('user_id')).first()
            if company is None:
                return Response({"status":"false","message":"Company not exists!"}, status=status.HTTP_400_BAD_REQUEST)

            data = {
                "company_id": company.id,
                "type":request.data.get('type'),
                "name":request.data.get('name'),
                "position":request.data.get('position'),
                "facebook_link":request.data.get('facebook_link'),
                "instagram_link":request.data.get('instagram_link'),
                "linked_in_link":request.data.get('linked_in_link'),
                "description":request.data.get('description'),
                "profile_image":request.data.get('profile_image'),
                "created_at":datetime.datetime.now()
            }
            serializer = Peopleserializer(data=data)
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
            people = People.objects.filter()
            serializer = Peopleserializer(people, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        try:
            people = People.objects.get(id = request.data.get('people_id'))
            if request.data.get('type'):
                people.type = request.data.get('type')
            if request.data.get('name'):
                people.name = request.data.get('name')
            if request.data.get('position'):
                people.position = request.data.get('position')
            if request.data.get('facebook_link'):
                people.facebook_link = request.data.get('facebook_link')
            if request.data.get('instagram_link'):
                people.instagram_link = request.data.get('instagram_link')
            if request.data.get('linked_in_link'):
                people.linked_in_link = request.data.get('linked_in_link')
            if request.data.get('description'):
                people.description = request.data.get('description')
            if request.data.get('profile_image'):
                people.profile_image = request.data.get('profile_image')
                 
            people.save()
            updated_people = People.objects.get(id = request.data.get('people_id'))
            serializer = Peopleserializer(updated_people, many=False)
            return Response({"status":"true","message":"People updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except People.DoesNotExist:
            return Response({"status":"false","message":"People Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
