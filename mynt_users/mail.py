from django.shortcuts import render
from mailjet_rest import Client
from rest_framework.response import Response
from django.template.loader import render_to_string
import os

# api_key = os.getenv('MJ_APIKEY_PUBLIC', "383e0aa03e6c11ea586113dfeb6f3b32")
# api_secret = os.getenv('MJ_APIKEY_PRIVATE', "6f53eddbf7f2c7d99001db8f7006d157")

# print(api_key, api_secret)

def send_mail(template_name, context, email, name, subject, text_part):
    # context = {
    # 'email': 123}

    html = render_to_string(template_name, context)
    api_key = '5e1fb5315223146aa61e51286d723328'
    api_secret = '80cb3e4f71079a3d2d19aa28596d456e'
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
