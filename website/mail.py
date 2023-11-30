from mailjet_rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.getenv('MJ_APIKEY_PRIVATE')
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
sender_email = "headliners@wangify.com"

def send_message(template_id = 5313119, barber_name = "Headliners Barbershop", first_name = "User", message = "default", user_email = None):
	data = {
	'Messages': [
			{
				"From": {
					"Email": sender_email,
					"Name": "Headliners Barbershop"
				},
				"To": [
					{
						"Email": user_email,
						"Name": "User"
					}
				],
				"TemplateID": template_id,
				"TemplateLanguage": True,
				"Subject": "You have a new message from [[data:barber_name:""]]",
				"Variables": {
		"firstname": first_name,
		"barber_name": barber_name,
		"message": message
	}
			}
		]
	}
	result = mailjet.send.create(data=data)
	print (result.status_code)
	print (result.json())


