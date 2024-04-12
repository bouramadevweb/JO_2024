import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


def envoie_sms(user_code):
    
    message = client.messages.create(
        body=f'Hi there {user_code}',
        from_='+13346001254',
        to='+33650255412',
    )
    print(message.sid)