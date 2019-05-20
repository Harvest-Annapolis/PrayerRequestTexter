#To Run: gunicorn --certfile server.crt --keyfile server.key -b 0.0.0.0:8443 web_application:app
from flask import Flask
from flask import render_template
from flask import request
import jsonpickle

app = Flask(__name__)

@app.route('/')
def index():
    """
    Renders the homepage.
    """
    return render_template('index.html')
    
@app.route("/test_info", methods=["POST"])
def test_twilio():
    f = open("/tmp/testme.txt", "w")
    f.write(jsonpickle.encode(request.form))
    f.close()
    return render_template('success.html') 

if __name__ == "__main__":
    app.run()
