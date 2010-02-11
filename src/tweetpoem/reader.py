#!/usr/bin/env python

import time
from getpass import getpass
from textwrap import TextWrapper
import re

import tweepy


class StreamWatcherListener(tweepy.StreamListener):

	status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
	what = None
	SPACE = re.compile("[\\s\\.:,]+")

	def on_status(self, status):

		try:
			article = False
			for word in self.SPACE.split(status.text):
				if word == '':
					continue
				if word == 'the':
					article = True
				else:
					if article:
						article = False
						what = word.translate(None,'"?!\'@#()[]{}\\').lower()
						if self.what != None and self.what != what:
							print "I don't like the %s, i'd rather the %s" % (self.what, what)
						self.what = what
			#print '\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source)
		except:
			# Catch any unicode errors while printing to console
			# and just ignore them to avoid breaking application.
			pass

	def on_error(self, status_code):
		print 'An error has occured! Status code = %s' % status_code
		return True  # keep stream alive

	def on_timeout(self):
		print 'Snoozing Zzzzzz'

def main():
	# Prompt for login credentials and setup stream object
	username = raw_input('Twitter username: ')
	password = getpass('Twitter password: ')
	stream = tweepy.Stream(username, password, StreamWatcherListener(), timeout=None)

	stream.sample()
if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print '\nGoodbye!'