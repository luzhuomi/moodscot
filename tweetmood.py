#from __future__ import absolute_import

#from workers.celery import celery
import subprocess, re, os, json, sys, sets 

from workers.tasks import princess, diva, monkey, anger, normal
import urllib2, threading
from dateutil.parser import parse
#from espeak import espeak
from datetime import datetime
from time import sleep

from twython import TwythonStreamer # easy_install twython

import urllib, urllib2
import simplejson


def get_mood(text):
	mood = None
	try:
		text = urllib.quote_plus(text,' ')
		#print text
		response = urllib2.urlopen("http://172.20.192.113/moodsense.org/MoodAnalyzer/Classifier?content=" + text)
		result = response.read()
		#print result
		# s = re.sub(r"- Classifier.*",'', response.read())
		# s = re.sub(r"<title>[^<]*</title>", "", s)
		# print s
		obj = simplejson.loads(result)
		# print obj
		if obj.has_key('moodBean'):
			#sleep(1)
			mbean = obj['moodBean']
			if mbean.has_key('mood'):
				mood = mbean['mood']
				if mood == "Undefined":
					mood = None
				   
	except Exception,e:
		print str(e)
	print "mood ="+str(mood)
	return mood


def act(data):
    try:
        if data.has_key("text"):
            # todo get the mood
            text = data["text"]	
	    text = mask_sensitive(text.lower())
            text = text.encode("ascii", "ignore")
	    main_routine(text)
            print "%s" % text
    except ValueError,e:
        pass

def mask_sensitive(text):
	x = text
	mask_mapping = {
		'fucking':' ', 'fuck':' ', 'shit':' ', 'cunt':' ', 'bitches':' ', 'cb':' ', 'knn':' ', 
		'knnccb':' ', 'bitch':' ', 'dick':' ', 'dickhead':' ', 'pussy':' ', 'fucked':' ', 'wtf':' ',
		'stfu':' ', 'whore':' ', 'slut':' ', 'asshole':' ', 'fcuking':' ', '_l_':' '	
	}

	for key, value in mask_mapping.items():
		x = x.replace(key,value)
	return x
'''
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
'''


def speak_and_act(mood, text):

	if mood == "joy":
		print "test"
		character = "princess"
		princess.delay(character,mood,text)
	elif mood == "sadness":
		character = "diva"
		diva.delay(character,mood,text)
	elif mood == "disgusted":
		character = "normal"
		normal.delay(character,mood,text)
	elif mood == "anger":
		character = "anger"
		anger.delay(character,mood,text)
	elif mood == "surprised":
		character = "monkey"
		monkey.delay(character,mood,text)

	#speak(text)
	#cmd = str(characters[character][mood])
	
	#send_perl_cmd(cmd)


def main_routine(text):
	# 1) make an api call to the mood analyzer API
	mood = get_mood(text)
	
	# 2) based on the mood (probably you need a if-else block)
	#    send the cmd to the furby
	if mood is not None:
	# send_cmd(mood, "monkey")
		speak_and_act(mood,text)





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

