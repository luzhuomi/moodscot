from __future__ import absolute_import

from workers.celery import celery
import subprocess, re, os, json, sys, sets 
import urllib2, threading
from dateutil.parser import parse
#from espeak import espeak
from datetime import datetime
from time import sleep

from twython import TwythonStreamer # easy_install twython

import urllib, urllib2
import simplejson


DEVNULL = open(os.devnull, 'wb')

def send_perl_cmd(cmd):
	#perl_script = "/home/charmaine/moodscot/workers/furby-send.pl"
	perl_script = "/home/pi/Desktop/moodscot/workers/furby-send.pl"
	pipe = subprocess.Popen(["perl", perl_script, cmd], stdin=subprocess.PIPE)
	pipe.stdin.close()
	return

def send_play_cmd(cmd):
	pipe = subprocess.Popen(["play", "/home/pi/Desktop/moodscot/wav/"+cmd+".wav"], stdin=subprocess.PIPE)
	pipe.stdin.close()
	return

# todo call perl library to perform wav sound generation and control furby
#      call espeak/festival to speak out the text

def speak(text):
	t = re.sub(r"http://[^ ]*", "", text)
	t = re.sub(r"rt", "", t)
	t = re.sub(r"@[^ ]*", "", t)
	t = re.sub(r"#[^ ]*", "", t)
	t = re.sub(r"^^", "", t)
	t = re.sub(r"&amp;", "", t)
	# espeak.synth(t)
	cast = "m2"
	speed = "125"
	# pipe = subprocess.Popen(["espeak", "-s", speed, "-v", cast, t,], stdin=subprocess.PIPE,  stdout=DEVNULL, stderr=DEVNULL)
	pipe = subprocess.Popen(["festival", "-b", "(SayText \"" + t + "\")"], stdin=subprocess.PIPE,  stdout=DEVNULL, stderr=DEVNULL)
	while pipe.poll() == None:
		sleep(0.5)
	pipe.stdin.close()
	return


characters = { 
  "princess" : { "joy" : 713, "sadness" : 861, "disgusted" : 714 }, 
  "angry" : { "joy" : 716 , "disgusted" : 714, "anger" : 871 },
  "diva" : { "joy" : 713, "sadness" : 861, "disgusted" : 714 },
  "monkey" : { "joy" : 716 , "surprised" : 858, "sadness" : 861, "disgusted" : 714 },
  "normal" : { "joy" : 716, "sadness" : 861, "disgusted" : 714 } }





@celery.task
def princess(character, mood, text):

	speak(text)
	cmd = str(characters[character][mood])
	
	send_play_cmd(cmd)

	

	print "princess in %s :%s :%s " % (character,mood,text)

@celery.task
def monkey(character,mood,text):
	speak(text)
	cmd = str(characters[character][mood])
	
	send_play_cmd(cmd)

	print "monkey in %s :%s :%s " % (character, mood,text)


@celery.task
def anger(character,mood,text):
	speak(text)
	cmd = str(characters[character][mood])
	
	send_play_cmd(cmd)
	print "angry in %s :%s :%s " % (character, mood,text)


@celery.task
def diva(character,mood,text):
	speak(text)
	cmd = str(characters[character][mood])
	
	send_play_cmd(cmd)
	print "diva in %s :%s :%s" % (character,mood,text)


@celery.task
def normal(character,mood,text):
	speak(text)
	cmd = str(characters[character][mood])
	
	send_play_cmd(cmd)
	print "normal in %s :%s :%s" % (character,mood,text)

