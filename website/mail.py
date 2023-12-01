import mailtrap as mt
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('MAILTRAP_TOKEN')
sender_email = "Headliners@wangify.com"

<<<<<<< HEAD
def send_email_notification(recipient_email, recipient_name, sender_name, message_content, role,):

	mail = mt.MailFromTemplate(
		sender=mt.Address(email=sender_email, name="Headliners Barbershop"),
		to=[mt.Address(email=recipient_email)],
		template_uuid="af3fdce7-f363-427c-9ba5-b757ef2d79b8",
  		template_variables={
			"sender_name": sender_name,
			"user": recipient_name,
			"subject": ("New message from ", sender_name),
			"message_content": message_content
 	    }
	)
=======
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
>>>>>>> parent of 9075323 (cleared db for demo)

	client = mt.MailtrapClient(token=token)
	client.send(mail)

