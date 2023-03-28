from mailjet_rest import Client
import os

api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.getenv('MJ_APIKEY_PRIVATE')

print(api_key, api_secret)

# mailjet = Client(auth=(api_key, api_secret), version='v3')
# data = {
#   'Author': "John Doe",
#   'Categories': "array",
#   'Copyright': "Mailjet",
#   'Description': "Used to send out promo codes.",
#   'EditMode': "1",
#   'IsStarred': "false",
#   'IsTextPartGenerationEnabled': "true",
#   'Locale': "en_US",
#   'Name': "Promo Codes",
#   'OwnerType': "user",
#   'Presets': "string",
#   'Purposes': "array"
# }
# result = mailjet.template.create(data=data)
# print result.status_code
# print result.json()