import pycurl, json, urllib2, sys, sets
from dateutil.parser import parse
from common.utils import *


from espeak import espeak # apt-get install python-espeak espeak
from datetime import datetime
from time import sleep

import piface.pfio

#STREAM_URL = "https://stream.twitter.com/1/statuses/filter.json?follow="
STREAM_URL = "https://stream.twitter.com/1/statuses/filter.json?track="


def speak(text):
    espeak.synth(text)

def move(unit):
    piface.pfio.digital_write(1, 1)
    sleep(unit)
    piface.pfio.digital_write(1, 0)


def analyze(data):
    try:
        data_json = json.loads(data)
        if data_json.has_key("text"):
            text = data_json["text"]
            speak(text)
            move(len(text)/5 + 1)
            print "%s" % text
    except ValueError,e:
        pass

def on_receive(data):
    #data_json = json.loads(data)
    #print data    
    analyze(data)

if len(sys.argv) < 1:
    print "Usage: stream.py <cred_file> <terms_file>"
    sys.exit(1)


#user_ids = get_userids_file(sys.argv[2])
terms = get_terms_file(sys.argv[2])

piface.pfio.init()

def loop(retry):
    try:
        cred = read_cred(sys.argv[1])
        conn = pycurl.Curl()
        conn.setopt(pycurl.USERPWD, "%s:%s" % (cred['user'], cred['password']))
        # conn.setopt(pycurl.URL, STREAM_URL+','.join(map(str,user_ids)))
        conn.setopt(pycurl.URL, STREAM_URL+','.join(map(str,terms)))
        conn.setopt(pycurl.WRITEFUNCTION, on_receive)
        conn.perform()
    except:
        if retry > 0:
            print "="*20
            print "retrying..."
            loop(retry-1)
        else:
            print "="*20            
            print "no more retry, exiting..."
            sys.exit(0)

loop(5)

