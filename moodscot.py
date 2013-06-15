import pycurl, json, urllib2, sys, sets, re
from dateutil.parser import parse
from common.utils import *


from espeak import espeak # apt-get install python-espeak espeak
from datetime import datetime
from time import sleep

from twython import TwythonStreamer # easy_install twython
def speak(text):
    t = re.sub(r"http://[^ ]*", "", text)
    t = re.sub(r"@", "", t)
    t = re.sub(r"#", "", t)
    espeak.synth(t)

'''
import piface.pfio

def move(unit):
    piface.pfio.digital_write(1, 1)
    sleep(max(1,unit/4))
    piface.pfio.digital_write(1, 0)


piface.pfio.init()
'''

def speak_and_move(text):
    speak(text)
    words = text.split(' ')
    move(len(words)+1)    

def act(data):
    try:
        if data.has_key("text"):
            # todo get the mood
            text = data["text"]
            # speak_and_move
            print "%s" % text
    except ValueError,e:
        pass


if len(sys.argv) < 1:
    print "Usage: python moodscot.py <cred_file> <terms>"
    sys.exit(1)

espeak.set_voice("f1") # female
# piface.pfio.init()


cred = read_cred(sys.argv[1])


client_args = {
    'verify': False
}

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
	act(data)

    def on_error(self, status_code, data):
        print status_code, data


stream = MyStreamer(cred['consumer_key'], cred['consumer_secret'],
                    cred['access_token_key'], cred['access_token_secret'],client_args=client_args)


keywords = sys.argv[2]
stream.statuses.filter(track=keywords)


