## A script to display live bus arrivals on InkyPhat
#import inky libraries
from inky import InkyPHAT

inky_display = InkyPHAT("black")

inky_display.set_border(inky_display.WHITE)

from PIL import Image, ImageFont, ImageDraw

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

from font_fredoka_one import FredokaOne

font = ImageFont.truetype(FredokaOne, 15)
##import python libraries for code cloned from github.com/m24murray/london-bus-arrivals
import os, requests
from datetime import datetime
from dotenv import load_dotenv
from os.path import join, dirname

load_dotenv('.env')
app_id = os.getenv('api id')
app_key = os.getenv('API key')
stop_id = os.getenv('490006192S')

##draw grid for inkyphat display
draw.line((1, 34, 212, 34), 1)       # Vertical line
draw.line((1, 68, 212, 68), 1)      # Horizontal top line
draw.line((1, 102, 212, 102), 1)      # Horizontal middle line

#obtain bus arrival info from tfl api (also from m24murray)
url = 'https://api.tfl.gov.uk/StopPoint/490006192S/arrivals'
params = {'app_id': app_id, 'app_key': app_key}

r = requests.get(url, params=params)
buses = r.json()

sorted_buses = []
for b in buses:
    sorted_buses.append({'bus': b[u'lineName'], 'destinationName': b[u'destinationName'], 'arrival': datetime.strptime(b[u'timeToLive'], '%Y-%m-%dT%H:%M:%S%fZ')})

sorted_buses = sorted(sorted_buses, key=lambda k: k['arrival'])
##truncate sorted buses to just next three arrivals
sorted_busestrun = sorted_buses[0:3]
#print(sorted_busestrun) #unhash to see full string

#return buses to console, this is as far as ive got
for ix, bus in enumerate(sorted_busestrun, 1):

    time = (bus['arrival'] - datetime.now()).seconds / 60
    if time < 1:
        disptime = "Due"
    elif time < 2:
        disptime = "1 Min"
    else:
        disptime = "{} Mins".format(int(time))
    dest = bus['destinationName'].split(',')[0]
    print("{} {}: {}".format(bus['bus'], dest, disptime))

#attempt to draw output to phat, breaks output image lines 
for ix, bus in enumerate(sorted_busestrun, 1):

    time = (bus['arrival'] - datetime.now()).seconds / 60
    if time < 1:
        disptime = "Due"
    elif time < 2:
        disptime = "1 Min"
    else:
        disptime = "{} Mins".format(int(time))
    dest = bus['destinationName'].split(',')[0]

    draw.text ((1, ix*34-33)  ((bus['bus'], dest), inky_display.BLACK, font=font) #2nd coord should start at 1 and increase by 34 to move each output down phat screen
    draw.text ((160, ix*34-33)  (disptime), inky_display.BLACK, font=font) #2nd coord should start at 1 and increase by 34 to move each output down phat screen

#dummy data to demonstrate phat output
#draw.text((1, 1), "E1", inky_display.BLACK, font=font) 
#draw.text((25, 1), "Ealing Broadway", inky_display.BLACK, font=font)
#draw.text((160, 1), "2 Mins", inky_display.BLACK, font=font)

#draw.text((1, 34), "E3", inky_display.BLACK, font=font) 
#draw.text((25, 34), "Chiswick", inky_display.BLACK, font=font)
#draw.text((160, 34), "4 Mins", inky_display.BLACK, font=font)

#draw.text((1, 68), "E1", inky_display.BLACK, font=font) 
#draw.text((25, 68), "Ealing Broadway", inky_display.BLACK, font=font)
#draw.text((160, 68), "11 Mins", inky_display.BLACK, font=font)

#output image to inkyphat
inky_display.set_image(img)
inky_display.show()

