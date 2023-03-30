from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from company.models import Company
from .models import Documents
from .serializers import DocumentsSerializer
from mynt_users.models import MyntUsers
from mynt_users.authentication import SafeJWTAuthentication
import datetime


class DocumentsApiView(APIView):
    permission_classes = [SafeJWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            company = Company.objects.get(id = request.data.get('company_id'))

            data = {
                "company_id":company.id,
                "document_type":request.data.get('document_type'),
                "document_name":request.data.get('document_name'),
                "agreement_status":request.data.get('agreement_status'),
                "created_at":datetime.datetime.now()
                }
            
            serializer = DocumentsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        try:
            documents = Documents.objects.filter()
            serializer = DocumentsSerializer(documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        try:
            
            document = Documents.objects.get(id = request.data.get('document_id'))

            if request.data.get('document_type'):
                document.document_type = request.data.get('document_type')

            if request.data.get('document_name'):
                document.document_name = request.data.get('document_name')

            if request.data.get('agreement_status'):
                document.agreement_status = request.data.get('agreement_status')
            
            if request.data.get('company_id'):
                company = Company.objects.filter(id = request.data.get('company_id')).first()
                if company:
                    document.company_id = company
                else:
                    return Response({"status":"false","message":"Company Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
            
            document.save()
            updated_document = Documents.objects.get(id = request.data.get('document_id'))
            serializer = DocumentsSerializer(updated_document, many=False)
            return Response({"status":"true","message":"Document updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except Documents.DoesNotExist:
            return Response({"status":"false","message":"Document Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    