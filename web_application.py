#To Run: gunicorn --certfile server.crt --keyfile server.key -b 0.0.0.0:8443 web_application:app
from flask import Flask
from flask import render_template
from flask import request
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
    
    cust = Customer.get_or_none(Customer.phone_number == phone_number) 
    if cust == None:
        cust = Customer(phone_number=phone_number)    
        cust.save()
    f = open("/tmp/testme.txt", "w")
    f.write(phone_number)
    f.write(message_content)
    f.write(cust.created_date.strftime("%Y-%m-%d %H:%M:%S"))
    f.write(cust.execute_time.strftime("%H:%M:%S"))
    f.write(cust.last_run_date.strftime("%Y-%m-%d"))
    f.write(str(cust.enabled))
    return render_template('success.html') 

if __name__ == "__main__":
    app.run()
