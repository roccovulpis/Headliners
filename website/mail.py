from mailjet_rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.getenv('MJ_APIKEY_PRIVATE')
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
  'Messages': [
		{
			"From": {
				"Email": "headliners@wangify.com",
				"Name": "Headliners Barbershop"
			},
			"To": [
				{
					"Email": "iwang.rgb@gmail.com",
					"Name": "User"
				}
			],
			"TemplateID": 5313119,
			"TemplateLanguage": True,
			"Subject": "You have a new message from [[data:firstname:""]]",
			"Variables": {
    "firstname": "",
    "barber_name": "barber name",
    "message": "message"
  }
		}
	]
}
result = mailjet.send.create(data=data)
print (result.status_code)
print (result.json())