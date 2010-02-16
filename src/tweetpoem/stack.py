#!/usr/bin/env python

from datetime import datetime, timedelta

class Stack(object):
	def __init__(self, maxage = 30):
		"maxage in second"
		self.maxage = timedelta(0, maxage)
		self.birth = datetime.now()
		self.data = {}
		self.keys = []
	def tick(self):
		return datetime.now() - self.birth
	def append(self, data):
		tick = self.tick()
		self.data[tick] = data
		self.keys.append(tick)
	def __iter__(self):
		now = self.tick()
		for k in self.keys:
			if now - k > self.maxage:
				self.keys.remove(k)
				del self.data[k]
			else:
				yield self.data[k]
	def since(self, when):
		now = time.clock()
		for k in self.keys:
			if now - k > self.maxage:
				self.keys.remove(k)
				del self.data[k]
			else:
				if k > when:
					yield self.data[k]

if __name__ == '__main__':
	import time
	s = Stack(3)
	for a in range(20):
		s.append(a)
	assert range(20) == list(s)
	print s.keys
	time.sleep(5)
	assert 0 == len(list(s))
