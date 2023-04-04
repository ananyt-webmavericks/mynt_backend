from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage
from rest_framework import status

class UploadFiles(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            file = request.data.get('file')
            # save file
            file_name = default_storage.save(file.name, file)

            # read file
            file_url = default_storage.url(file_name)

            #create url for file
            base_url = request.build_absolute_uri('/')[:-1]
            url = f"{base_url}{file_url}"

            return Response({"status":"true","message": str(url)},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)