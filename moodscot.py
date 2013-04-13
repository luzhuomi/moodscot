import pycurl, json, urllib2, sys, sets
from dateutil.parser import parse

from common.utils import *


STREAM_URL = "https://stream.twitter.com/1/statuses/filter.json?follow="


def analyze(data):
    try:
        data_json = json.loads(data)
        if data_json.has_key("text"):
            text = data_json["text"]
            print "%s" % text
    except ValueError,e:
        pass

def on_receive(data):
    #data_json = json.loads(data)
    print data    
    analyze(data)

if len(sys.argv) < 1:
    print "Usage: stream.py <user_id file>"
    sys.exit(1)

user_ids = get_userids_file(sys.argv[2])

def loop(retry):
    try:
        cred = read_cred(sys.argv[1])
        conn = pycurl.Curl()
        conn.setopt(pycurl.USERPWD, "%s:%s" % (cred['user'], cred['password']))
        conn.setopt(pycurl.URL, STREAM_URL+','.join(map(str,user_ids)))
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
