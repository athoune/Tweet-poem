#!/usr/bin/env python

import time
from getpass import getpass
from textwrap import TextWrapper
import re
import cStringIO

import tweepy

class ScreamingBag(object):
	def append(self, strophe):
		print strophe

def clean(word):
	#[FIXME] is it the best way?
	output = cStringIO.StringIO()
	for l in word:
		if l not in u'"?!\'@#()[]{}\\':
			output.write(unicode(l).encode('utf8'))
	return unicode(output.getvalue(), 'utf8')

class StreamWatcherListener(tweepy.StreamListener):

	status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
	what = None
	SPACE = re.compile("[\\s\\.:,]+")
	
	def __init__(self, bag = ScreamingBag()):
		tweepy.StreamListener.__init__(self)
		self.bag = bag
		
#	def on_data(self, data):
#		print data
#		tweepy.StreamListener.on_data(self, data)

	def on_status(self, status):
		article = False
		for word in self.SPACE.split(status.text):
			if word == '':
				continue
			if word == 'the':
				article = True
				continue
			if article:
				article = False
				what = clean(word).lower()
				if self.what != None and self.what != what:
					self.bag.append(u"I don't like the " + self.what + u", i'd rather the " + what)
				self.what = what

	def on_error(self, status_code):
		print 'An error has occured! Status code = %s' % status_code
		return True  # keep stream alive

	def on_timeout(self):
		print 'Snoozing Zzzzzz'

def poem(username, password, async=False, bag=ScreamingBag()):
	stream = tweepy.Stream(username, password, StreamWatcherListener(bag), timeout=None, retry_count=10)
	try:
		stream.sample(async=async)
	except KeyboardInterrupt:
		print "stop it!"
		stream.disconnect()

def main():
	# Prompt for login credentials and setup stream object
	username = raw_input('Twitter username: ')
	password = getpass('Twitter password: ')
	poem(username, password)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print '\nGoodbye!'