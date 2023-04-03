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
from mynt_users.authentication import SafeJWTAuthentication
import datetime


class HighlightsApiView(APIView):
    permission_classes = [SafeJWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            campaign = Campaign.objects.get(id = request.data.get('campaign_id'))

            highlights = request.data.get('highlights')
            errors = []
            res_data = []
            if isinstance(highlights, list):
                for i in highlights:
                    try:
                        data = {
                                "campaign_id": campaign.id,
                                "title":i['title'],
                                "description":i['description'],
                                "created_at":datetime.datetime.now()
                            }
                        serializer = Highlightsserializer(data=data)
                        if serializer.is_valid():
                            serializer.save()
                            res_data.append(serializer.data)
                        else:
                            errors.append(serializer.errors)

                    except Exception as e:
                        continue
            else:
                return Response({"status":"false","message":"Invalid format of property highlights!"}, status=status.HTTP_400_BAD_REQUEST)
                
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(res_data, status=status.HTTP_201_CREATED)
            
        except Campaign.DoesNotExist:
            return Response({"status":"false","message":"Campaign Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
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

            if request.data.get('status'):
                highlight.status = request.data.get('status')

            if request.data.get('campaign_id'):
                campaign = Campaign.objects.filter(id = request.data.get('campaign_id')).first()
                if campaign:
                    highlight.campaign_id = campaign
                else:
                    return Response({"status":"false","message":"Campaign Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
                 
            highlight.save()
            updated_highlight = Highlights.objects.get(id = request.data.get('highlight_id'))
            serializer = Highlightsserializer(updated_highlight, many=False)
            return Response({"status":"true","message":"Highlight updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except Highlights.DoesNotExist:
            return Response({"status":"false","message":"Highlight Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetHighlightsbyCampaignId(APIView):
    permission_classes = [SafeJWTAuthentication]

    def get(self, request, id):
        try:
            highlights = Highlights.objects.filter(campaign_id = id).all()
            if highlights:
                serializer = Highlightsserializer(highlights, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"status":"false","message":"Highlights Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)