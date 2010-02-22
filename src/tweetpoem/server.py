#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.escape import json_encode

import os
import sys

from redistack import RedisTack

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		return self.render('data/index.html')

class PoemHandler(tornado.web.RequestHandler):
	stack = RedisTack()
	@tornado.web.asynchronous
	def get(self):
		self.set_header("Content-Type", "application/json")
		since = self.get_argument("since", None)
		while True:
			if since == None:
				data = list(self.stack)
			else:
				data = list(self.stack.since(int(since)))
			if data != []:
				break
			time.sleep(1)
		self.write('{"poems":[')
		size = len(data)
		cpt = 0
		tick = None
		for a in data:
			cpt += 1
			tick, poem = a.split(':', 1)
			self.write(json_encode(poem))
			if cpt < size:
				self.write(',')
		self.write('],"tick":%s}' %tick)
		self.finish()

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "data"),
	"gzip": True
}
application = tornado.web.Application([
    (r"/", MainHandler, {}),
	(r"/poem", PoemHandler)
], **settings)

def main(port):
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(port)
	print "open http://localhost:%i\n" % port
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main(int(sys.argv[1]))