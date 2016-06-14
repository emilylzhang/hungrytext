from flask import Flask, request, redirect, send_from_directory
import twilio.twiml
import os
# import googlemaps
import geocoder

# googlemaps key
# it was here before i took it out

# Download the twilio-python library from http://twilio.com/docs/libraries
# from twilio.rest import TwilioRestClient

# create a client object to use Yelp API
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

auth = Oauth1Authenticator(
    consumer_key = os.getenv('YELP_CONSUMER_KEY'),
    consumer_secret = os.getenv('YELP_CONSUMER_SECRET'),
    token = os.getenv('YELP_YOUR_KEY'),
    token_secret = os.getenv('YELP_YOUR_SECRET')
)

client = Client(auth)

# create a Flask app
app = Flask(__name__)

# begin here
@app.route("/", methods=['GET'])
def kek():
    return "READ THE FUCKING DOCUMENTATION U FUCKING SLUT"

@app.route("/", methods=['POST'])
def hello():
    """Respond to incoming calls with a simple text message."""
    resp = twilio.twiml.Response()

    # get the number that the request is from
    from_number = request.values.get('From', None)
    # get the body of the text message
    body = request.values.get('Body')

    # debugging info
    print("number: " + from_number)
    print("body: " + body)

    # # Geocoding an address
    geocode_result = geocoder.google(body)
    # print("geocode_result: " + geocode_result)
    print(geocode_result.latlng)
    lat = geocode_result.latlng[0]
    lng = geocode_result.latlng[1]
    latlng = str(geocode_result.latlng).strip('[]')

    resp.message("yo, this is what you wrote: " + body +"\nAnd this is the latitude and longitude of the location you texted: (" +latlng +")")
    # below is when i was using the google geocoding api -
        # geocode_result = gmaps.geocode(body)
        # print("geocode_result: " + geocode_result)
        # print("formatted address: " + geocode_result.formatted_address)

    print("response: " + str(resp))
    return str(resp)

# handle favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/png/vnd.microsoft.icon')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.config.update(DEBUG=True)
    app.run(host='0.0.0.0', port=port)
