#!/usr/bin/env python

from datetime import datetime, timedelta

from redis import Redis

class RedisTack(object):
	"One writer, n readers"
	def __init__(self, host= 'localhost', port=6379, db=0, max=30, purge=False):
		self.redis = Redis(host=host, port=port, db=db)
		self.max = max
		self.DATA = 'data'
		self.IDX = 'idx'
		if purge:
			self.redis.flushdb()
	def append(self, data):
		#[TODO] add a transaction
		idx = int(self.redis.incr(self.IDX))
		pipe = self.redis.pipeline()
		pipe.rpush(self.DATA, '%i:' % idx + data).ltrim(self.DATA, -self.max, -1)
		pipe.execute()
	def __iter__(self):
		return iter(self.redis.lrange(self.DATA, 0, -1))
	def idx(self):
		return int(self.redis[self.IDX])
	def since(self, when):
		for a in  self.redis.lrange(self.DATA, 0, -1):
			idx, data = a.split(':', 1)
			if int(idx) > when:
				yield a
if __name__ == '__main__':
	stack = RedisTack(purge=True, max=20)
	for a in range(20):
		stack.append(str(a))
	print list(stack)
	assert ['%i:%i' %(a+1,a) for a in range(20)] == list(stack)
	print list(stack.since(15))
	print stack.idx()
	stack.append("20")
	assert ['%i:%i' %(a+1,a) for a in range(1, 21)] == list(stack)
