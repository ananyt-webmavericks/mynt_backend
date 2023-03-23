from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DealType
from .serializers import DealTypeSerializer
import datetime


class DealTypeApiView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            deal_type = DealType.objects.filter(deal_name = request.data.get('deal_name'))
            if deal_type:
                return Response({"status":"false","message":"Deal Type already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                "deal_name":request.data.get('deal_name'),
                "created_at":datetime.datetime.now()
                }
            serializer = DealTypeSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        try:
            deal_type = DealType.objects.filter()
            serializer = DealTypeSerializer(deal_type, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        try:
            deal_type = DealType.objects.get(id = request.data.get('deal_type_id'))
            deal_name = DealType.objects.filter(deal_name = request.data.get('deal_name'))
           
            if deal_name:
                return Response({"status":"false","message":"Deal Name already exists!"}, status=status.HTTP_400_BAD_REQUEST)

            if request.data.get('deal_name'):
                deal_type.deal_name = request.data.get('deal_name')
            
                     
            deal_type.save()
            updated_deal_type = DealType.objects.get(id = request.data.get('deal_type_id'))
            serializer = DealTypeSerializer(updated_deal_type, many=False)
            return Response({"status":"true","message":"Deal Type updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except DealType.DoesNotExist:
            return Response({"status":"false","message":"Deal Type Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
   
