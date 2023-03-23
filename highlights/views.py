from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from company.models import Company
from campaign.models import Campaign
from .models import Highlights
from .serializers import Highlightsserializer
from mynt_users.models import MyntUsers
import datetime


class HighlightsApiView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(id = request.data.get('user_id'))
            company = Company.objects.filter(user_id = request.data.get('user_id')).first()
            if company is None:
                return Response({"status":"false","message":"Company not exists!"}, status=status.HTTP_400_BAD_REQUEST)

            campaign = Campaign.objects.filter(company_id = company).first()
            if campaign is None:
                return Response({"status":"false","message":"Campaign not exists!"}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                "campaign_id": campaign.id,
                "title":request.data.get('title'),
                "description":request.data.get('description'),
                "highlight_image":request.data.get('highlight_image'),
                "created_at":datetime.datetime.now()
            }
            serializer = Highlightsserializer(data=data)
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
            highlights = Highlights.objects.filter()
            serializer = Highlightsserializer(highlights, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        try:
            highlight = Highlights.objects.get(id = request.data.get('highlight_id'))
            if request.data.get('title'):
                highlight.title = request.data.get('title')
            if request.data.get('description'):
                highlight.description = request.data.get('description')
            if request.data.get('highlight_image'):
                highlight.highlight_image = request.data.get('highlight_image')
                 
            highlight.save()
            updated_highlight = Highlights.objects.get(id = request.data.get('highlight_id'))
            serializer = Highlightsserializer(updated_highlight, many=False)
            return Response({"status":"true","message":"Highlight updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except Highlights.DoesNotExist:
            return Response({"status":"false","message":"Highlight Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
