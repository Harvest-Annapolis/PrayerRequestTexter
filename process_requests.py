#!/usr/bin/env python3
from parse_requests import get_message
from send_message import send_message
from db_repo import *
import datetime

print("Here")
custs = Customer.select().where(Customer.enabled and 
                                  Customer.last_run_date < datetime.date.today() and 
                                  Customer.execute_time < datetime.datetime.now().time())
prayer_request = get_message()

print(len(custs))
for cust in custs:    
    cust.last_run_date = datetime.date.today()
    cust.save()
    
    status = send_message(cust.phone_number, prayer_request)
    print(status)
