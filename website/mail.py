import mailtrap as mt
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('MAILTRAP_TOKEN')
sender_email = "Headliners@wangify.com"

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

	client = mt.MailtrapClient(token=token)
	client.send(mail)

