#!/usr/bin/env python

import time

class Stack(object):
	def __init__(self, maxage = 30):
		"maxage in second"
		self.maxage = maxage
		self.data = {}
		self.keys = []
	def append(self, data):
		tick = time.clock()
		self.data[tick] = data
		self.keys.append(tick)
	def __iter__(self):
		now = time.clock()
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
	s = Stack(30)
	for a in range(20):
		s.append(a)
	assert range(20) == list(s)
	print s.keys
