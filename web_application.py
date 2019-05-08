from gevent.pywsgi import WSGIServer
from flask import Flask

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    """
    Renders the homepage.
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.config["SECRET_KEY"] = "ITSASECRET"
    http_server = WSGIServer(('', 5000), app, keyfile='key.pem', certfile='cert.pem')
    http_server.serve_forever()