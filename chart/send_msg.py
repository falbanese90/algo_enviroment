from config import twilio_sid, twilio_auth, twilio_number
from twilio.rest import Client

client = Client(twilio_sid, twilio_auth)

def send_error(msg):
    client.messages.create(body=msg, from_=twilio_number, to='+16313009484')