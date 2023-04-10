from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Company
from mynt_users.models import MyntUsers
from .serializers import CompanySerializers
from mynt_users.authentication import SafeJWTAuthentication
import datetime

class CompanyApiView(APIView):
    permission_classes = [SafeJWTAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            company = Company.objects.filter()
            serializer = CompanySerializers(company, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        try:
            company = Company.objects.get(id = request.data.get('company_id'))
            if request.data.get('company_logo'):
                company.company_logo = request.data.get('company_logo')
            if request.data.get('founder_linked_in_profile'):
                company.founder_linked_in_profile = request.data.get('founder_linked_in_profile')
            if request.data.get('company_name'):
                company.company_name = request.data.get('company_name')
            if request.data.get('company_linked_in_profile'):
                company.company_linked_in_profile = request.data.get('company_linked_in_profile')
            if request.data.get('website_url'):
                company.website_url = request.data.get('website_url')
            if request.data.get('previous_funding'):
                company.previous_funding = request.data.get('previous_funding')
            if request.data.get('product_description'):
                company.product_description = request.data.get('product_description')
            if request.data.get('traction_description'):
                company.traction_description = request.data.get('traction_description')
            if request.data.get('revenue'):
                company.revenue = request.data.get('revenue')
            if request.data.get('reason_for_community_round'):
                company.reason_for_community_round = request.data.get('reason_for_community_round')
            if request.data.get('reason_for_mynt'):
                company.reason_for_mynt = request.data.get('reason_for_mynt')
            if request.data.get('existing_commitments'):
                company.existing_commitments = request.data.get('existing_commitments')
            if request.data.get('company_pitch'):
                company.company_pitch = request.data.get('company_pitch')
            if request.data.get('country'):
                company.country = request.data.get('country')
            if request.data.get('state'):
                company.state = request.data.get('state')
            if request.data.get('city'):
                company.city = request.data.get('city')
            if request.data.get('pincode'):
                company.pincode = request.data.get('pincode')
            if request.data.get('company_address'):
                company.company_address = request.data.get('company_address')
            if request.data.get('status'):
                company.status = request.data.get('status')
            if request.data.get('facebook_link'):
                 company.facebook_link = request.data.get('facebook_link')
            if request.data.get('instagram_link'):
                 company.instagram_link = request.data.get('instagram_link')
            if request.data.get('legal_name'):
                 company.legal_name = request.data.get('legal_name')
            if request.data.get('cin'):
                 company.cin = request.data.get('cin')
            if request.data.get('date_of_incorporation'):
                 company.date_of_incorporation = request.data.get('date_of_incorporation')
            if request.data.get('incorporation_type'):
                 company.incorporation_type = request.data.get('incorporation_type')
            if request.data.get('sector'):
                 company.sector = request.data.get('sector')
            if request.data.get('invested_so_far'):
                 company.invested_so_far = request.data.get('invested_so_far')
            if request.data.get('number_of_employees'):
                 company.number_of_employees = request.data.get('number_of_employees')
            if request.data.get('number_of_employees'):
                 company.number_of_employees = request.data.get('number_of_employees')
            if request.data.get('number_of_employees'):
                 company.number_of_employees = request.data.get('number_of_employees')
            
                     
            company.save()
            updated_company = Company.objects.get(id = request.data.get('company_id'))
            serializer = CompanySerializers(updated_company, many=False)
            return Response({"status":"true","message":"Company updated successfully!","data":serializer.data}, status=status.HTTP_200_OK)

        except Company.DoesNotExist:
            return Response({"status":"false","message":"Company Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CompanyCreateApiView(APIView):
     
     def post(self, request, *args, **kwargs):
        try:
            user = MyntUsers.objects.get(id = request.data.get('user_id'))
            company = Company.objects.filter(user_id = request.data.get('user_id'))
            if company:
                return Response({"status":"false","message":"Company already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            data = {
                "company_logo":request.data.get('company_logo'),
                "founder_linked_in_profile": request.data.get('founder_linked_in_profile'),
                "company_name":request.data.get('company_name'),
                "company_linked_in_profile":request.data.get('company_linked_in_profile'),
                "website_url":request.data.get('website_url'),
                "previous_funding":request.data.get('previous_funding'),
                "product_description":request.data.get('product_description'),
                "traction_description":request.data.get('traction_description'),
                "revenue":request.data.get('revenue'),
                "reason_for_community_round":request.data.get('reason_for_community_round'),
                "reason_for_mynt":request.data.get('reason_for_mynt'),
                "existing_commitments":request.data.get('existing_commitments'),
                "company_pitch":request.data.get('company_pitch'),
                "created_at":datetime.datetime.now(),
                "user_id": user.id
            }
            serializer = CompanySerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class GetCompanyByUserId(APIView):
    permission_classes = [SafeJWTAuthentication]

    def get(self, request, id):
        try:
            user = MyntUsers.objects.get(id=id)
            company = Company.objects.filter(user_id = user.id).first()
            if company is None:
                return Response({"status":"false","message":"Company Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
            
            serializer = CompanySerializers(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MyntUsers.DoesNotExist:
            return Response({"status":"false","message":"User Doesn't Exist!"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)