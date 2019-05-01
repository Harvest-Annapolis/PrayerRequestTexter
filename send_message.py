#!/usr/bin/env python3
from twilio.rest import Client
from secure impotr auth_token
account_sid = "AC28f029f16dbfe40db0e3282072153ecc"
client = Client(account_sid, auth_token)
message = client.messages.create(
    to="+13347968921", 
    from_="+14432929313",
    body="Hello from Python!")
print(message.sid)
