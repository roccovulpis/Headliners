from mailjet_rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.getenv('MJ_APIKEY_PRIVATE')
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
sender_email = "headliners@wangify.com"

def send_email_notification(recipient_email, recipient_name, sender_name, message_content, role, template_id=5313119):

	subject = f"You have a new message from {sender_name}"
	if role == 'barber':
		subject = (f"New client message from {sender_name}")
	     
	data = {
			'Messages': [
				{
					"From": {
						"Email": sender_email,
						"Name": "Headliners Barbershop"
					},
					"To": [
						{
							"Email": recipient_email,
							"Name": recipient_name
						}
					],
					"TemplateID": template_id,
					"TemplateLanguage": True,
					"Subject": subject,
					"Variables": {
						"firstname": recipient_name,
						"barber_name": sender_name,
						"message": message_content
					}
				}
			]
		}
	result = mailjet.send.create(data=data)
	print(result.status_code)
	print(result.json())


