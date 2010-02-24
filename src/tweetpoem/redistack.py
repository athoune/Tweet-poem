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
		idx = self.redis.incr(self.IDX)
		pipe = self.redis.pipeline()
		pipe.set(idx,  data).expire(idx, 30)
		pipe.execute()
	def all(self):
		idx = int(self.redis.get(self.IDX))
		return self.since(max(1, idx - self.max))
	def since(self, when):
		idx = int(self.redis.get(self.IDX))
		return idx, self.redis.mget([str(a) for a in range(max(when+1, idx -self.max +1 ), idx+1)])
if __name__ == '__main__':
	stack = RedisTack(purge=True, max=20)
	for a in range(1, 21):
		stack.append(str(a))
	print stack.all()
	#assert [str(a) for a in range(20)] == list(stack)
	print "since 15", list(stack.since(15))
	stack.append("21")
	idx, values =  stack.all()
	assert 20 == len(values)
	print values
	assert [str(a) for a in range(2, 22)] == values

