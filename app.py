# from laurenorsini on github, used as a tutorial

from flask import Flask 
from flask import render_template
from flask import request, redirect

from twilio.rest import TwilioRestClient 

app = Flask(__name__) # Creating the Flask app
client = TwilioRestClient ('TWILIO_ACCOUNT_SID = os.environ['ACeea7e767ce9bd7c44be45b3ce491fed5']', 'TWILIO_AUTH_TOKEN = os.environ['4b4f9277b2c60150c0a1f5233cee287e']') # Paste in your AccountSID and AuthToken here
twilio_number = "+16696005660" # Replace with your Twilio number

@app.route("/") # When you go to top page of app, this is what it will execute
def main():
    return render_template('form.html')
  
@app.route("/submit-form/", methods = ['POST']) 
def submit_number():
    number = request.form['number']
    formatted_number = "+1" + number # Switch to your country code of choice
    client.messages.create(to=formatted_number, from_ = twilio_number, body = "I will send you the location of the nearest In-&-Out. What is your current location?") # Replace body with your message of choice
    return redirect('/messages/')
  
@app.route("/messages/")
def list_messages():
    messages = client.messages.list(to=twilio_number)
    return render_template('messages.html', messages = messages)
    

if __name__ == '__main__': # If we're executing this app from the command line
    app.run("0.0.0.0", port = 3000, debug = True)


    
# Find these values at https://twilio.com/user/account
# account_sid = "ACeea7e767ce9bd7c44be45b3ce491fed5"
# auth_token = "4b4f9277b2c60150c0a1f5233cee287e"
# client = TwilioRestClient(account_sid, auth_token)

# message = client.messages.create(to="+12316851234", from_="+16696005660",
#                                      body="so....")
