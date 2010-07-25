#!/usr/bin/env python

from getpass import getpass

from redistack import RedisTack
from reader import poem


def main(login, password):
	poem(login, password, bag=RedisTack(debug=True))

if __name__ == "__main__":
	name = raw_input('Twitter username: ')
	passwd = getpass('Twitter password: ')
	main(name, passwd)