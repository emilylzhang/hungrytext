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

# create a Flask app
app = Flask(__name__)

# begin here
@app.route("/", methods=['GET'])
def kek():
    return "READ THE FUCKING DOCUMENTATION U FUCKING SLUT AHHHHhhHH"

@app.route("/", methods=['POST'])
def hello():
    print(os.getenv('YELP_CONSUMER_KEY'))
    lat = 0
    lng = 0
    burgeraddr = 0

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
    print(0)

    if lat != 0 and lng != 0:
        print(1)
        auth = Oauth1Authenticator(
            consumer_key=os.getenv('YELP_CONSUMER_KEY'),
            consumer_secret=os.getenv('YELP_CONSUMER_SECRET'),
            token=os.getenv('YELP_TOKEN_KEY'),
            token_secret=os.getenv('YELP_TOKEN_SECRET')
        )
        print(2)
        client = Client(auth)
        print(3)
        params = {
            'term': 'In-N-Out Burger',
            'lang': 'en',
            'limit': 1,     # limit 1 business result
            'sort': 0,      # sort by best match
            'category_filter': 'burgers'
        }
        print(4)
        burgerplace = client.search_by_coordinates(lat, lng, **params)
        print(5)
        burgeraddr = burgerplace.businesses[0].location.display_address
        address = ""
        while len(burgeraddr) != 0:
            address = burgeraddr.pop() + ", " + address
        address = address[0:len(address)-2]
        print(address)

    resp.message("yo, this is the location of the nearest In-N-Out: " +address)

    # resp.message("yo, this is what you wrote: " +body +"\nAnd this is the latitude and longitude of the location you texted: (" +latlng +")\nAnd this is the address of the nearest In-N-Out: " +burgeraddr)
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
