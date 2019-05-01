#!/usr/bin/env python3
from parse_requests import get_message
from send_message import send_message

numbers = [ "+13347968921" , "+15867702894" ]
prayer_request = get_message()

for phone in numbers:
    status = send_message(phone, prayer_request)
    print(status)
