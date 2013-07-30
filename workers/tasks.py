from __future__ import absolute_import

from workers.celery import celery


@celery.task
def princess(mood,text):
	print "princess in %s :%s " % (mood,text)

@celery.task
def monkey(mood,text):
	print "monkey in %s :%s " % (mood,text)


@celery.task
def angry(mood,text):
	print "angry in %s :%s " % (mood,text)


@celery.task
def diva(mood,text):
	print "diva in %s :%s " % (mood,text)


@celery.task
def normal(mood,text):
	print "normal in %s :%s " % (mood,text)

