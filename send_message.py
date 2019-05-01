#!/usr/bin/env python3
from twilio.rest import Client
from secure import auth_token, account_sid, account_number
def send_message(to, content):
    account_sid = account_sid
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=to, 
        from_=account_number,
        body=content)
    return message.status
