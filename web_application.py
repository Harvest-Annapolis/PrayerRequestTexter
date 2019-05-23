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
    # Parse data from request.
    phone_number = request.form["phone_number"]
    message_content = request.form["message_content"]
    
    # Variable defaults
    send_welcome = False
    
    #Get the customer that's texting.
    cust = Customer.get_or_none(Customer.phone_number == phone_number) 
    
    # Make a new customer if one doesn't exist.
    if cust == None:
        cust = Customer(phone_number=phone_number)    
        cust.save(force_insert=True)
        send_welcome = True
                
    # Re-enable a previously disabled customer.
    if not cust.enabled and ("yes" in message_content.lower() or "subscribe" in message_content.lower()):
        send_welcome = True
        cust.enabled = True
        cust.save()
        
    # Parse out the time they want to receive texts    
    time_value = "".join([i for i in message_content if i.isdigit()])
    if len(time_value) <= 6:
        good_time = False
        if len(time_value) in [1, 2]:
            hrs = int(time_value)
            mins = 0
        elif len(time_value) in [3, 5]:
            hrs = int(time_value[0])
            mins = int(time_value[1:3])
        elif len(time_value) in [4, 6]:
            hrs = int(time_value[0:2])
            mins = int(time_value[2:4])

        if hrs < 24 and mins < 60:
            if "pm" in message_content.lower() and hrs < 12:
                hrs += 12
            cust.execute_time = datetime.datetime(2000,1,1,hrs,mins,0).time()
            cust.save()

        if not send_welcome:
            status = send_message(cust.phone_number, "You have adjusted the time you receive the daily prayer text to {}.".format(cust.execute_time.strftime("%I:%M %p")))
    # Unsubscribe
    elif "stop" in message_content.lower() or "unsubscribe" in message_content.lower():
        cust.enabled = False
        cust.save()
    # Command not recognized
    elif not send_welcome:
        status = send_message(cust.phone_number, "Sorry, I don't recognize that command.")
    # Send a welcome message if they havent gotten one before.
    elif send_welcome:
        status = send_message(cust.phone_number, "Thank you for subscribing to the Harvest Prayer Request text list.  You will currently receive a daily prayer request at {}.  To change this time, simply reply with the time you would prefer.  To stop these messages, simply reply STOP.".format(cust.execute_time.strftime("%I:%M %p")))
    
    # Make sure they get today's message if the time they picked hasn't passed yet.
    if datetime.datetime.now() < datetime.datetime.combine(datetime.datetime.now().date(), cust.execute_time):
        cust.last_run_date = datetime.date.today() - datetime.timedelta(days=1)
        cust.save()
    else:
        cust.last_run_date = datetime.date.today()
        cust.save()
    
    return render_template('success.html') 

if __name__ == "__main__":
    app.run()
