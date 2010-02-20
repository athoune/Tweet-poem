#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.escape import json_encode

from datetime import timedelta
from getpass import getpass
import os
import time

import reader
from stack import Stack

def str2td(txt):
	n = txt.split(':')
	return timedelta(int(n[0]), int(n[1]), int(n[2]))
def td2str(td):
	return "%i:%i:%i" % (td.days, td.seconds, td.microseconds)

class StackBag(object):
	def __init__(self, size=30):
		self.stack = Stack(size)
	def append(self, line):
		#print line
		self.stack.append(line)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")

class PoemHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		global stack
		self.set_header("Content-Type", "application/json")
		since = self.get_argument("since", None)
		if since == None:
			tick = stack.stack.tick()
		else:
			tick = str2td(since)
		while True:
			if since == None:
				data = list(stack.stack)
			else:
				data = list(stack.stack.since(tick))
			if data != []:
				break
			time.sleep(1)
		self.write(json_encode({'tick': td2str(tick), 'poems': data}))
		self.finish()

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "data"),
	"gzip": True
}
application = tornado.web.Application([
    (r"/", MainHandler),
	(r"/poem", PoemHandler),
], **settings)

def main(login, password):
	global stack
	stack = StackBag(30)
	reader.poem(login, password, async=True, bag=stack)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	print "open http://localhost:8888\n"
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	username = raw_input('Twitter username: ')
	password = getpass('Twitter password: ')
	main(username, password)