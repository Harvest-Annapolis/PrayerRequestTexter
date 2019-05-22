#To Run: gunicorn --certfile server.crt --keyfile server.key -b 0.0.0.0:8443 web_application:app
from flask import Flask
from flask import render_template
from flask import request
from send_message import send_message
from db_repo import *

app = Flask(__name__)

@app.route('/')
def index():
    """
    Renders the homepage.
    """
    return render_template('index.html')
    
@app.route("/test_info", methods=["POST"])
def test_twilio():
    phone_number = request.form["phone_number"]
    message_content = request.form["message_content"]
    
    send_welcome = False
    cust = Customer.get_or_none(Customer.phone_number == phone_number) 
    if cust == None:
        cust = Customer(phone_number=phone_number)    
        cust.save(force_insert=True)
        send_welcome = True
    
    time_value = "".join([i for i in message_content if i.isdigit()])
    if len(time_value) in [2, 4, 6]:
        if len(time_value) == 2:
            hrs = int(time_value)
            if hrs < 24:
                if "pm" in message_content.lower() and hrs < 12:
                    hrs += 12
                cust.execute_time = datetime.datetime(2000,1,1,hrs,0,0).time
                cust.save()
        elif len(time_value) == 4 || len(time_value) == 6:
            hrs = int(time_value[0:2])
            mins = int(time_value[2:4])
            if hrs < 24 and mins < 60:
                if "pm" in message_content.lower() and hrs < 12:
                    hrs += 12
                cust.execute_time = datetime.datetime(2000,1,1,hrs,mins,0).time
                cust.save()
        if not send_welcome:
            status = send_message(cust.phone_number, "You have adjusted the time you receive the daily prayer text to {}.".format(cust.execute_time.strftime("%I:%M %p")))
     elif "stop" in message_content.lower() or "unsubscribe" in message_content.lower()
        cust.enabled = False
        cust.save()
        status = send_message(cust.phone_number, "You have been unsubscribed.  If you ever want to re-subscribe, simply text us with the time you would like to get your daily prayer requests.")
     elif not send_welcome:
        status = send_message(cust.phone_number, "Sorry, I don't recognize that command.")
     elif send_welcome:
        status = send_message(cust.phone_number, "Thank you for subscribing to the Harvest Prayer Request text list.  You will currently receive a daily prayer request at {}.  To change this time, simply reply with the time you would prefer.  To stop these messages, simply reply STOP.".format(cust.execute_time.strftime("%I:%M %p")))
    
    return render_template('success.html') 

if __name__ == "__main__":
    app.run()
