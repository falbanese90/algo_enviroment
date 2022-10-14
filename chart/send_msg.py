from config import twilio_sid, twilio_auth, twilio_number
from twilio.rest import Client

## Establish Twilio SMS Connections
client = Client(twilio_sid, twilio_auth)

def send_error(msg):
    ''' Sends Logged Error to my Phone '''
    client.messages.create(
        body=f'{msg}', 
        from_=twilio_number, 
        to='+00000000000'
        )