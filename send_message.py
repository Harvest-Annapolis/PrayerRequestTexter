#!/usr/bin/env python3
from twilio.rest import Client
from secure import auth_token
def send_message(to, content):
    account_sid = "AC28f029f16dbfe40db0e3282072153ecc"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=to, 
        from_="+14432929313",
        body=content)
    return message.status
