from flask import Flask, request, redirect, send_from_directory
import twilio.twiml
import os

# import googlemaps and geocoder
import geocoder
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key=os.getenv('GOOGLE_SERVER_API_KEY'))

# download the twilio-python library from http://twilio.com/docs/libraries
# and create a client object to use the twilio REST api
from twilio.rest import TwilioRestClient

twilioclient = TwilioRestClient(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN')) 

# create a client object to use Yelp API
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

auth = Oauth1Authenticator(
    consumer_key=os.getenv('YELP_CONSUMER_KEY'),
    consumer_secret=os.getenv('YELP_CONSUMER_SECRET'),
    token=os.getenv('YELP_TOKEN_KEY'),
    token_secret=os.getenv('YELP_TOKEN_SECRET')
)
yelpclient = Client(auth)
params = {
    'term': 'In-N-Out Burger',
    'lang': 'en',
    'limit': 1,     # limit 1 business result
    'sort': 0,      # sort by best match
    'category_filter': 'burgers'
}

# create a Flask app
app = Flask(__name__)

# begin here
@app.route("/", methods=['GET'])
def kek():
    return "Yo, you should try texting (669) 600-5660"

@app.route("/", methods=['POST'])
def hello():
    lat = 0
    lng = 0
    burgeraddr = 0

    # respond to incoming calls with a simple text message
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

    # if POST request has been made with proper lat and lng
    if lat != 0 and lng != 0:
        burgerplace = yelpclient.search_by_coordinates(lat, lng, **params)
        if len(burgerplace.businesses) != 0:
            burgeraddr = burgerplace.businesses[0].location.display_address
            address = ""
            while len(burgeraddr) != 0:
                address = burgeraddr.pop() + ", " + address
            address = address[0:len(address)-2]
            print(address)
        else:
            address = "YOU DID NOT GIVE A VALID ADDRESS"

    # create response message
    # text(from_number, "yo, this is the location of the nearest In-N-Out: " +address)
    resp.message("...............................\n\n\nyo, this is the location of the nearest In-N-Out: " +address)

    # text directions to the nearest In-n-Out
    directions(from_number, address, body)

    print("response: " + str(resp))
    return str(resp)

# finds directions to the nearest In-N-Out
def directions(number, to_address, from_address):
    now = datetime.now()
    directions_result = gmaps.directions(origin=from_address,
                                     destination=to_address,
                                     mode="driving",
                                     departure_time=now)
    leg = directions_result[0]['legs']
    steps = leg[0]['steps']
    directiontext = ""
    for i in range(0, len(steps)):
        # test the part below
        step = steps[i]['html_instructions']
        print(step)
        step = remove_html_markup(step)
        directiontext = directiontext +str(i+1) +") " +step +"\n\n"
    text(number, directiontext)

# sends a text to the number given, with textbody as the content
def text(number, textbody):
    twilioclient.messages.create(
        to=number, 
        from_="+16696005660", 
        body="...............................\n\n\n"+textbody, 
        media_url="http://media2.fdncms.com/sacurrent/imager/new-headline/u/slideshow/2346373/in-n-out-burger.jpg", 
    )

# remove HTML tags from the directions
# taken from http://stackoverflow.com/a/14464381
def remove_html_markup(s):
    tag = False
    quote = False
    out = ""
    div1 = False
    div2 = False

    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif (c == '"' or c == "'") and tag:
            quote = not quote
        elif not tag:
            out = out + c
        elif tag and c == 'd':
            div1 = True
        elif tag and div1 and c == 'i':
            div2 = True
        elif tag and div1 and div2 and c == 'v':
            out = out + "\n"
            div1 = False
            div2 = False
        else:
            div1 = False 
            div2 = False

    return out

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
