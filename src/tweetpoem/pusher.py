#!/usr/bin/env python

from getpass import getpass

from redistack import RedisTack
import reader



def main(login, password):
	stack = RedisTack()
	reader.poem(login, password, async=False, bag=stack)
	
if __name__ == "__main__":
	username = raw_input('Twitter username: ')
	password = getpass('Twitter password: ')
	main(username, password)