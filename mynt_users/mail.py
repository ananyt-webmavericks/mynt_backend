from django.shortcuts import render
from mailjet_rest import Client
from rest_framework.response import Response
from django.template.loader import render_to_string
from rest_framework import status
import os
import environ
env = environ.Env()
environ.Env.read_env()

def send_mail(template_name, context, email, name, subject, text_part):
    try:
        html = render_to_string(template_name, context)
        api_key = "5e1fb5315223146aa61e51286d723328"
        api_secret = "80cb3e4f71079a3d2d19aa28596d456e"
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
        'Messages': [
            {
            "From": {
                "Email": "ananya@thesoftcoders.com",
                "Name": "Meteor Ventures"
            },
            "To": [
                {
                "Email": email,
                "Name": name
                }
            ],
            "Subject": subject,
            "TextPart": text_part,
            "HTMLPart": html

            }
        ]
        }
        result = mailjet.send.create(data=data)
        # print(result.status_code)
        # print(result.json())
    
    except Exception as e:
            return Response({"status":"false","message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
