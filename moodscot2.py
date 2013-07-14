'''
reference 
https://github.com/tweepy/tweepy/issues/172


sudo vim requests-1.2.3-py2.7.egg/requests/packages/urllib3/util.py

line 28
from ssl import wrap_socket, CERT_NONE, PROTOCOL_SSLv23, PROTOCOL_SSLv3


line 297 
return PROTOCOL_SSLv3
'''


import subprocess
import re
import os
import pycurl, json, sys, sets 
import urllib2
from dateutil.parser import parse
from espeak import espeak
from datetime import datetime
from time import sleep

from twython import TwythonStreamer # easy_install twython


DEVNULL = open(os.devnull, 'wb')

def speak(text):
    t = re.sub(r"http://[^ ]*", "", text)
    t = re.sub(r"RT", "", t)
    t = re.sub(r"@[^ ]*", "", t)
    t = re.sub(r"#[^ ]*", "", t)
    # espeak.synth(t)
    cast = "m2"
    speed = "125"
    pipe = subprocess.Popen(["espeak", "-s", speed, "-v", cast, t,], stdin=subprocess.PIPE,  stdout=DEVNULL, stderr=DEVNULL)
    while pipe.poll() == None:
        sleep(0.5)
    pipe.stdin.close()
    return


def act(data):
    try:
        if data.has_key("text"):
            # todo get the mood
            text = data["text"]
            print "%s" % text
            speak(text)
    except ValueError,e:
        pass


def read_cred(file):
    in_handle = open(file,'r')
    cred = {}
    for ln in in_handle:
        data = ln.strip('\r\n').split('=')
        if len(data) > 1:
            key = data[0].strip(' ').lower()
            value = data[1].strip(' ')
            cred[key] = value
        else:
            print "error in parsing credentials file"
    return cred


espeak.set_voice("f1") # female


cred = read_cred(sys.argv[1])

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
    act(data)

    def on_error(self, status_code, data):
        print status_code, data


stream = MyStreamer(cred['consumer_key'], cred['consumer_secret'],
                    cred['access_token_key'], cred['access_token_secret'])


keywords = sys.argv[2]

stream.statuses.filter(track=keywords)

'''
INSTALLING FESTIVAL

sudo apt-get install festival festlex-cmu festlex-poslex festlex-oald libestools1.2 unzip
apt-cache search festvox-*
sudo apt-get install festvox-don festvox-rablpc16k festvox-kallpc16k festvox-kdlpc16k

pipe = subprocess.Popen(["festival", "-b", "(SayText \"" + t + "\")"], stdin=subprocess.PIPE,  stdout=DEVNULL, stderr=DEVNULL)
'''


import urllib2
import simplejson 

def get_mood(text):
    response = urllib2.urlopen("http://172.20.192.113/moodsense.org/MoodAnalyzer/Classifier?content=" + text)
    obj = simplejson.loads(response.read())
    mood = None
    if obj.has_key('moodBean'):
        mbean = obj['moodBean']
        if mbean.has_key('mood'):
            mood = mbean['mood']
    return mood

'''
The sample moodsense API:
http://172.20.192.113/moodsense.org/MoodAnalyzer/Classifier?content=i%20am%20happy
 
 
http://172.20.192.113/moodsense.org/MoodAnalyzer/Classifier?content=xxxxxx where xxxx is the input content
and the output in JSON format:
{'moodBean':{{'content':'i am happy','mood':'sadness'}}

'''
