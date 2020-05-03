# Prayer Request Texter
Welcome to the Harvest Annapolis Prayer Request Texter.  This project has two overarching pieces.  A web server that takes requests and manages a database of clients (customers) to send the prayer request text messages to, and a program that runs as a once a minute cron job that actually sends the messages out.

The web server is Flask, fronted by Gunicorn, and is installed as a systemd service on a Raspberry Pi.

This repo leaves out the keys, certs, and the database of customer information (for obvious reasons), but I will detail how to generate those below.

## Supporting files

So, some supporting players.  These scripts are used for all parts of the system.

Components: 
 * db_repo.py
 * customer_data.db (not included)
 * send_message.py
 * secure.py (not included)

### db_repo.py
This guy handles all the database stuff.  It's using the ORM peewee to avoid having to fiddle with direct SQLite commands.  So, to get this to work, you're gonna have to do a "pip3 install peewee".  It's a great module though.  You can look up all the docs online, but I think this should be a pretty straightforward one.

As a note, if you run this file directly, it'll go ahead and just create your customer_data.db file for you.  Super easy there.

### customer_data.db
As previously stated, just run db_repo.py directly to make this guy.

He's a SQLite database, and he's awesome.  Not a whole lot more to say here.  I'd reccommend the program "sqlite3" if you need to fiddle with it directly, but like, that should be more of a troubleshooting thing than something you actually do.

### send_message.py
This guy is who actually handles sending text messages.  It does so through a service called Twilio.  Twilio charges, like, 0.004¢ per text.  It just leverages it via it's API.  Pretty straight forward.

You will need a "pip3 install twilio" to get this up and running.
 
### secure.py
This should be a file that contains your sensitive variables for interfacing with Twilio.  It should look something like this:
```python
auth_token  = "<your assigned Twilio auth token>"
account_sid = "<your assigned Twilio sid>"
account_number = "<your assigned Twilio number>",
```
 
## The Web Server

So, this is the bread and butter of the whole operation.  It's what handles signups, profile changes, the website form.  Basically everything but actually sending the final text.

Components: 
 * web_application.py
 * server.crt (not included)
 * server.key (not included)
 * templates/failure.html
 * templates/index.html
 * templates/success.html
 * templates/web_form.html
 
### web_application.py
This is the core of the operation.  It's the Flask server itself.

As before, we've got a few libraries, so you're gonna have to "pip3 install flask" and "pip3 install gunicorn".

To launch the web server, run the following:
gunicorn --certfile server.crt --keyfile server.key -b 0.0.0.0:8443 web_application:app

There's a few different things handled here.  First is the only post action, and that's what handles actually processing new requests coming in.  It checks to see if they're currently active, and if not, and they're saying they want to be, it sends a welcome message.  If the request is coming from the web form, it sends a "Press enter to continue" type thing to the user.  If it's a time, and they're currently active, it changes the time they're signed up for.  Etc.

Then there's the web_form bit.  That is what's rendered in an iframe on the https://harvestannapolis.org/prayer page.

That's the main stuff.  There's an index as well, but that's mostly there to just verify connectivity.

### server.crt and server.key
This should be super straightforward.  Basically just go here:
https://certbot.eff.org/lets-encrypt/debianstretch-other
and follow instructions.

server.crt will be your "fullchain.pem" file, and server.key will be your "privkey.pem" file.  Those should be located in the /etc/lets-encrypt/live/your_domain/ folder.

You will need a domain name for that, so like, get to it.

### templates/*
Everything here are just html templates.  They're actually just served statically.  I didn't even bother putting in, like, python directives or anything.  The only complicated one is the web_form one, just cause it's all fancy and bootstrappy.  But, like, I trust you to figure it out.
 
## The Text Sender

So this is the thing that actually sends the texts!

Components: 
 * process_requests.py
 * parse_requests.py
 
### process_requests.py
This is the guy who actually sends the texts.  It checks if the user has gotten a text that day already, and if the time they want the text has passed.  If yes to both, it sends them a text, then updates the database to reflect that they've gotten their daily message.

### parse_requests.py
This is actually pretty specific to Harvest Annapolis and also pretty fragile.  You'll probably want to change it if you're taking this elsewhere.

Basically, this is the thing that figures out what to send.  See, the way we're populating that is that Jason is putting the prayer requests in as a SquareSpace blog, and has them scheduled to go out every day at midnight. This is available as an RSS feed, so that's what we're parsing.

So, for this to work you'll need feedparser, so that's another "pip3 install feedparser".

## Installation

Before any of this, you'll probably have to do a "sudo apt-get install pip3".
Just to get the above listed python libraries (peewee, twilio, flask, gunicorn, and feedparser).
Then get those libraries.

Then you'll want to download the whole repo and put it in a directory somewhere.  Convention says probably in /opt/your_texting_program.

Then you'll want to run the db_repo.py to make the db.

Then you'll want to generate your certs.

Make your secure.py file.

Then test to make sure to give execute permissions to all the python files ("sudo chmod +x *.py")

Verify that you can launch the webserver manually.  (See above)

Install the web server as a service.
To do this, you'll need to create a service file.  So, here it goes:
vim /lib/systemd/system/twilio-server.service
Add the following:
```bash
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
WorkingDirectory=/opt/your_texting_program/
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:8443  --certfile server.crt --keyfile server.key web_application:app
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=Twilio_Server

[Install]
WantedBy=multi-user.target
```
Then:
vim /etc/rsyslog.d/twilio-server.conf
Add the following:
```bash
if $programname == 'Twilio_Server' then /var/log/text_manager/server.log
& stop
```
Then:
mkdir /var/log/text_manager
systemctl daemon-reload
systemctl enable twilio-server
reboot

Verify the service is running and listening on 8443:
netstat -antp

Now, you have to set up your Twilio to properly post data to it.  To do that, you're gonna go into your Twilio account, and go into "Studio."  Go to "Manage Flows", then your_flow_name. 

You're gonna add an "HTTP Request" module, then tie the "Incoming Message" trigger to it.  Set it to request method POST.  Set Request URL to the url of your POST method on the server.  Content Type = Form URL Encoded.  Http Parameters are [ phone_number : {{trigger.message.From}}, message_content : {{trigger.message.Body}}, web_submission : False ].

If you want to be thorough, you can tie the "Fail" trigger from your HTTP Request to a "Send Message" block, that will message your admin if the web server breaks.

Once all that's done, hit "Publish" at the top.

Then text your Twilio number a time, and see if you get a response.  If so, you did it!!

Then you just have to set up your cron to run the process_requests.py.  Just:
vim /etc/crontab
And add the following:
```bash
*  *    * * *   root    cd /opt/PrayerRequestTexter && ./process_requests.py 2>&1 | tee -a /var/log/text_manager/sender.log
```

systemctl restart cron 

Set your time to get the text 2min in the future (to be safe), then see if you get it.

If so, you should be good to go!!  Thanks for using our service!!!!  :) 