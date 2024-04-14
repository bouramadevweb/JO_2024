import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


def envoie_sms(user_code,phone_number):
    
    message = client.messages.create(
        body=f' bonjour votre code est {user_code}',
        from_='+13346001254',
        to=phone_number,
    )
    print(message.sid)