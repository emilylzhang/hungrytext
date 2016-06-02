from flask import Flask, request, redirect
import twilio.twiml
import os
# import googlemaps
import geocoder

# googlemaps key
# it was here before i took it out

# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# create a client object to use Yelp API
# from yelp.client import Client
# from yelp.oauth1_authenticator import Oauth1Authenticator


# client = Client(auth)

# create a Flask app
app = Flask(__name__)

# begin here
@app.route("/", methods=['GET', 'POST'])
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
    print(1)
    resp.message("yo, this is what you wrote: " + body)

    # Geocoding an address
    print(2) # debugging info
    geocode_result = geocoder.google(body)
    print("geocode_result: " + geocode_result)
    print("latitude and longitde: " +geocode_result.latlng)
    # below is when i was using the google geocoding api -
        # geocode_result = gmaps.geocode(body)
        # print("geocode_result: " + geocode_result)
        # print("formatted address: " + geocode_result.formatted_address)

    print("response" + str(resp))
    return str(resp)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)